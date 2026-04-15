import os
import json
import subprocess
import pdfplumber
from fastapi import FastAPI, UploadFile, File, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, FileSystemLoader

from keys import CHAVE_OPENROUTER
from openai import OpenAI

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=CHAVE_OPENROUTER)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurando o Jinja2 para não entrar em conflito com o LaTeX
latex_env = Environment(
    loader=FileSystemLoader("templates"),
    block_start_string=r'\BLOCK{',
    block_end_string='}',
    variable_start_string=r'\VAR{',
    variable_end_string='}',
    comment_start_string=r'\#{',
    comment_end_string='}',
)

def extrair_texto_pdf(arquivo_pdf):
    texto_completo = ""
    with pdfplumber.open(arquivo_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
    return texto_completo

def montar_prompt(modo, texto_cv, texto_vaga):
    if modo == "Gaps":
        return f"""
        Você é um recrutador técnico sênior. 
        Sua tarefa é cruzar os dados do currículo do candidato com os requisitos da vaga e gerar um relatório direto e realista.
        NÃO GERE UM CURRÍCULO. Gere apenas a análise.

        VAGA:
        {texto_vaga}

        CURRÍCULO:
        {texto_cv}

        Retorne ESTRITAMENTE um JSON com esta estrutura (sem marcações markdown como ```json):
        {{
          "nome": "Nome",
          "match": "Porcentagem de compatibilidade real (ex: 30%)",
          "resumo_analise": "Análise direta e sem rodeios sobre o nível do candidato versus o que a vaga pede.",
          "pontos_fortes": ["O que ele já tem"],
          "lacunas_criticas": ["Ferramentas ou experiências que faltam"],
          "plano_acao": ["Passo 1 realista para aprender até a entrevista", "Passo 2"]
        }}
        """
    else:
        base = f"""
        Você é um especialista em escrita de currículos para sistemas ATS e leitura humana rápida.
        Sua tarefa é reescrever o currículo do candidato com base na vaga fornecida.
        Retorne ESTRITAMENTE um JSON puro (sem markdown).

        DIRETRIZES DE ESTILO E ESCRITA (CRÍTICO):
        1. O texto deve ser específico, ativo, claro e objetivo. Sem floreios.
        2. Baseie-se em fatos: quantifique e qualifique resultados sempre que possível.
        3. Fale como um humano profissional. EVITE TERMINANTEMENTE palavras complexas ou jargões típicos de IA (como "alavancar", "orquestrar", "impulsionar", "sinergia", "panorama"). Use verbos de ação diretos (desenvolvi, criei, reduzi, implementei).
        4. Use o método STAR (Situação, Tarefa, Ação, Resultado) para criar os bullet points das experiências. Foque no impacto, não apenas nas tarefas.

        REGRAS DE ESTRUTURA:
        - Experiências: Ordene da mais recente para a mais antiga. Destaque habilidades transferíveis (comunicação, mentoria).
        - Habilidades: Seja curto. Apenas o que importa para a vaga.

        ESTRUTURA DO JSON OBRIGATÓRIA:
        {{
          "nome": "Nome do Candidato",
          "contato": "Cidade, Estado • email • linkedin • github",
          "resumo": "Um parágrafo direto, focado no que o candidato entrega de valor para a vaga.",
          "educacao": [
            {{
              "instituicao": "Nome da Instituição",
              "local": "Localização",
              "curso": "Nome do Curso",
              "data": "Mês/Ano - Mês/Ano"
            }}
          ],
          "experiencias": [
            {{
              "empresa": "Nome da Empresa",
              "local": "Localização",
              "cargo": "Nome do Cargo",
              "data": "Mês/Ano - Mês/Ano",
              "descricoes": ["Conquista com método STAR e métrica", "Outra conquista direta"]
            }}
          ],
          "habilidades_tecnicas": "Linguagens, frameworks e ferramentas essenciais",
          "idiomas": "Idioma (Nível)"
        }}

        VAGA:
        {texto_vaga}

        CURRÍCULO ORIGINAL:
        {texto_cv}
        """

        if modo == "Seguro":
            return base + """
            MODO: OTIMIZAÇÃO SEGURA.
            - Mantenha a verdade. Não invente anos de experiência que o candidato não tem.
            - Adapte as descrições dos projetos reais do candidato para "conversar" com as palavras-chave da vaga.
            - Adicione 1 ou 2 ferramentas principais da vaga de forma sutil, sugerindo que o candidato tem conhecimento base ou está estudando ativamente para a entrevista.
            """
        elif modo == "Inclusao":
            return base + """
            MODO: FULL MATCH.
            - Force a barra para gerar um currículo ideal para essa vaga.
            - Pegue as ferramentas e requisitos principais da vaga e INJETE-OS nas experiências passadas do candidato, criando bullet points usando o método STAR como se ele já tivesse longa experiência naquilo.
            """
        return base

@app.post("/api/upload")
async def processar_curriculo(
    file: UploadFile = File(...),
    vaga: str = Form(...),
    modo: str = Form(...)
):
    try:
        texto_extraido = extrair_texto_pdf(file.file)
        prompt_final = montar_prompt(modo, texto_extraido, vaga)

        resposta = client.chat.completions.create(
            model="google/gemini-2.5-flash", # Esse é o nome exato do modelo lá no OpenRouter
            messages=[
                {"role": "user", "content": prompt_final}
            ],
            response_format={"type": "json_object"} # Garante o retorno em JSON
        )
        texto_resposta = resposta.choices[0].message.content
        dados_json = json.loads(texto_resposta)
        
        # Função rápida para limpar caracteres que quebram o LaTeX
        def limpa_tex(texto):
            if not isinstance(texto, str): return texto
            for char in ['%', '&', '$', '#', '_']:
                texto = texto.replace(char, f'\\{char}')
            return texto

        if modo == "Gaps":
            template = latex_env.get_template("template_gaps.tex")
            tex_renderizado = template.render(
                nome=limpa_tex(dados_json.get("nome", "Candidato")),
                match=limpa_tex(dados_json.get("match", "")),
                resumo_analise=limpa_tex(dados_json.get("resumo_analise", "")),
                pontos_fortes=[limpa_tex(i) for i in dados_json.get("pontos_fortes", [])],
                lacunas_criticas=[limpa_tex(i) for i in dados_json.get("lacunas_criticas", [])],
                plano_acao=[limpa_tex(i) for i in dados_json.get("plano_acao", [])]
            )
        else:
            template = latex_env.get_template("template_basico.tex")
            tex_renderizado = template.render(
                nome=limpa_tex(dados_json.get("nome", "Nome não encontrado")),
                contato=limpa_tex(dados_json.get("contato", "")),
                resumo=limpa_tex(dados_json.get("resumo", "")),
                experiencias=[
                    {
                        "empresa": limpa_tex(exp.get("empresa", "")),
                        "local": limpa_tex(exp.get("local", "")),
                        "cargo": limpa_tex(exp.get("cargo", "")),
                        "data": limpa_tex(exp.get("data", "")),
                        "descricoes": [limpa_tex(d) for d in exp.get("descricoes", [])]
                    } for exp in dados_json.get("experiencias", [])
                ],
                habilidades_tecnicas=limpa_tex(dados_json.get("habilidades_tecnicas", "")),
                idiomas=limpa_tex(dados_json.get("idiomas", "")),
                educacao=[
                    {
                        "instituicao": limpa_tex(edu.get("instituicao", "")),
                        "local": limpa_tex(edu.get("local", "")),
                        "curso": limpa_tex(edu.get("curso", "")),
                        "data": limpa_tex(edu.get("data", ""))
                    } for edu in dados_json.get("educacao", [])
                ]
            )

        nome_base = "cv_temp"
        caminho_tex = f"{nome_base}.tex"
        with open(caminho_tex, "w", encoding="utf-8") as f:
            f.write(tex_renderizado)

        processo = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", caminho_tex],
            capture_output=True,
            text=True
        )

        if processo.returncode != 0:
            print("Erro no LaTeX:", processo.stdout)
            return Response(status_code=500, content="Erro ao compilar o PDF (LaTeX). Veja o terminal do backend.")

        with open(f"{nome_base}.pdf", "rb") as f:
            pdf_bytes = f.read()

        for ext in ['.tex', '.pdf', '.aux', '.log', '.out']:
            arq = f"{nome_base}{ext}"
            if os.path.exists(arq):
                os.remove(arq)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=curriculo_otimizado.pdf"
            }
        )

    except Exception as e:
        print("\n" + "="*30)
        print("🚨 ERRO DETALHADO 🚨")
        import traceback
        traceback.print_exc()
        print("="*30 + "\n")
        return Response(status_code=500, content=f"Erro geral: {str(e)}")