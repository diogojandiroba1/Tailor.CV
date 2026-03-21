import os
import json
import pdfplumber
import pdfkit # Importação nova!
from fastapi import FastAPI, UploadFile, File, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, FileSystemLoader
from google import genai
from keys import CHAVE_GEMINI
from google.genai import types

client = genai.Client(api_key=CHAVE_GEMINI)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env = Environment(loader=FileSystemLoader("templates"))

# --- CONFIGURAÇÃO DO PDFKIT PARA WINDOWS ---
# Se instalaste no caminho padrão, isto vai funcionar. Se mudaste, ajusta o caminho abaixo.
caminho_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config_pdfkit = pdfkit.configuration(wkhtmltopdf=caminho_wkhtmltopdf)
# -------------------------------------------

def extrair_texto_pdf(arquivo_pdf):
    texto_completo = ""
    with pdfplumber.open(arquivo_pdf) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
    return texto_completo

def montar_prompt(modo, texto_cv, texto_vaga):
    base = f"""
    Você é um assistente especialista em recrutamento e sistemas ATS.
    Sua tarefa é analisar o currículo abaixo e a descrição da vaga, e retornar um JSON estruturado.
    
    O JSON DEVE conter exatamente as seguintes chaves:
    - "Resumo": Um texto de apresentação otimizado.
    - "Experiencias": Uma lista de strings com as experiências profissionais reescritas.
    - "Habilidades": Uma lista de strings com as competências técnicas e comportamentais.

    Currículo do Candidato:
    {texto_cv}

    Descrição da Vaga:
    {texto_vaga}
    """
    if modo == "Gaps":
        return base + """\nMODO DE OPERAÇÃO: Analisador de Gaps.
        Compare o currículo com a vaga e crie um relatório do que falta. Sugira projetos acadêmicos ou pessoais para preencher essas lacunas."""
    elif modo == "Seguro":
        return base + """\nMODO DE OPERAÇÃO: Otimização Segura.
        Reescreva as experiências usando as palavras-chave da vaga para passar no filtro ATS. NÃO invente habilidades que o candidato não possua."""
    elif modo == "Inclusao":
        return base + """\nMODO DE OPERAÇÃO: Inclusão.
        Injete as palavras-chave da vaga no currículo, mesclando-as com as experiências do usuário de forma natural."""
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

        resposta = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_final,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )

        dados_json = json.loads(resposta.text)

        template = env.get_template("template_basico.html")
        
        html_renderizado = template.render(
            nome_candidato="Diogo", # Como sei que te chamas Diogo, já deixei preenchido ;)
            resumo=dados_json.get("Resumo", ""),
            experiencias=dados_json.get("Experiencias", []),
            habilidades=dados_json.get("Habilidades", [])
        )

        # Geração do PDF usando pdfkit!
        pdf_bytes = pdfkit.from_string(html_renderizado, False, configuration=config_pdfkit)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=curriculo_otimizado.pdf"
            }
        )

    except Exception as e:
        return Response(status_code=500, content=f"Erro: {str(e)}")