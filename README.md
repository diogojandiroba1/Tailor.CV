# Tailor.CV

Um utilitário alimentado por IA para otimizar, adequar e gerar currículos profissionais prontos para envio, com base em descrições de vagas específicas. O Tailor.CV ajuda candidatos a passarem pelos filtros de ATS (Applicant Tracking Systems) ajustando o conteúdo e formatando o resultado em templates aceitos pelo mercado.

## 🚀 Funcionalidades

O sistema possui fluxos de análise, otimização e formatação:

### 1. Modos de Operação
* **🔍 Analisador de Gaps (Gap Analyzer):** Compara o currículo atual com a vaga e gera um relatório do que está faltando. Sugere tópicos de estudo ou como aproveitar projetos acadêmicos e pessoais para preencher essas lacunas.
* **🛡️ Otimização Segura:** Reescreve as experiências *existentes* no currículo usando as palavras-chave da vaga, sem inventar nenhuma habilidade que o candidato não possua.
* **⚠️ Modo Inclusão:** Injeta as palavras-chave e habilidades exigidas pela vaga diretamente no currículo, mesclando-as com as experiências do usuário, independentemente de ele possuir a habilidade ou não.

### 2. Formatação e Exportação
* **🎨 Escolha de Templates:** O usuário pode selecionar entre diversos modelos de currículo (clássico, moderno, minimalista), todos projetados para serem **ATS-Friendly** (fáceis de ler por sistemas automatizados de recrutamento).
* **📥 Exportação Direta para PDF:** O sistema gera e permite o download imediato do novo currículo em formato PDF de alta qualidade, pronto para aplicação.

## 🛠️ Tecnologias Utilizadas

* **Frontend:** React, Next.js, Tailwind CSS (para a interface de seleção de templates e upload).
* **Backend:** Python, FastAPI.
* **Manipulação e Leitura de PDF:** `pdfplumber` (para extrair texto do CV original).
* **Inteligência Artificial:** API do Gemini (ou OpenAI) para PNL e reescrita de conteúdo.
* **Geração de PDF:** `Jinja2` (para templating HTML) e `WeasyPrint` (para conversão de HTML/CSS para PDF final).

## ⚙️ Como Funciona

1.  O usuário faz o upload do seu currículo em `.pdf` e cola a descrição da vaga.
2.  Seleciona o modo de operação da IA (Gaps, Otimização Segura ou Inclusão Forçada).
3.  O usuário escolhe um dos templates visuais disponíveis.
4.  O backend extrai o texto do PDF original e envia para o LLM com o prompt específico do modo selecionado.
5.  O LLM retorna o conteúdo do currículo otimizado.
6.  O backend pega esse conteúdo, aplica no template HTML/CSS escolhido usando Jinja2, e converte para PDF usando WeasyPrint.
7.  O usuário faz o download do PDF final.

## 💻 Instalação e Uso local

### Pré-requisitos
* Node.js instalado
* Python 3.10+
* Chave de API do LLM escolhido (ex: `GEMINI_API_KEY`)

### Rodando o Backend (FastAPI)
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

### Rodando o Frontend (Next.js)
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

## 📝 Próximos Passos / Melhorias Futuras
- [ ] Extensão para navegador que lê a vaga do LinkedIn e já puxa os dados automaticamente.
- [ ] Histórico de currículos gerados por usuário (com login).
