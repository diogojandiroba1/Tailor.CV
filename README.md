# Tailor.CV

Um utilitário alimentado por IA para otimizar, adequar e gerar currículos profissionais prontos para envio, com base em descrições de vagas específicas. O Tailor.CV ajuda candidatos a passarem pelos filtros de ATS (Applicant Tracking Systems) ajustando o conteúdo e formatando o resultado em templates aceitos pelo mercado.

## 🚀 Funcionalidades

O sistema possui fluxos de análise, otimização e formatação:

### 1. Modos de Operação
* **🔍 Analisador de Gaps (Gap Analyzer):** Compara o currículo atual com a vaga e gera um relatório do que está faltando. Sugere tópicos de estudo ou como aproveitar projetos acadêmicos e pessoais para preencher essas lacunas.
* **🛡️ Otimização Segura:** Reescreve as experiências *existentes* no currículo usando as palavras-chave da vaga, sem inventar nenhuma habilidade que o candidato não possua.
* **⚠️ Modo Inclusão:** Injeta as palavras-chave e habilidades exigidas pela vaga diretamente no currículo, mesclando-as com as experiências do usuário, independentemente de ele possuir a habilidade ou não.

### 2. Formatação e Exportação
* **🎨 Escolha de Templates:** O usuário pode selecionar entre modelos de currículo (clássico, moderno, minimalista), todos projetados para serem **ATS-Friendly** (fáceis de ler por sistemas automatizados de recrutamento).
* **📥 Exportação Direta para PDF:** O sistema gera e permite o download imediato do novo currículo em formato PDF de alta qualidade, pronto para aplicação.

## 🛠️ Tecnologias Utilizadas

* **Frontend:** React, Next.js, Tailwind CSS (para a interface de seleção de templates e upload).
* **Backend:** Python, FastAPI.
* **Manipulação e Leitura de PDF:** `pdfplumber` (para extrair texto do CV original).
* **Inteligência Artificial:** Google Gemini API (via SDK moderna `google-genai`).
* **Geração de PDF:** `Jinja2` (para templating HTML) e `pdfkit` com `wkhtmltopdf` (para conversão estável de HTML/CSS para PDF no Windows).

## ⚙️ Como Funciona

1.  O usuário faz o upload do seu currículo em `.pdf` e cola a descrição da vaga na interface Next.js.
2.  Seleciona o modo de operação da IA (Gaps, Otimização Segura ou Inclusão Forçada).
3.  O backend extrai o texto do PDF original e envia para o modelo `gemini-1.5-flash` com um prompt estruturado para retorno em JSON.
4.  O LLM retorna o conteúdo otimizado (Resumo, Experiências e Habilidades).
5.  O backend processa esses dados, aplica no template HTML escolhido via **Jinja2** e utiliza o **pdfkit** para gerar o binário do PDF.
6.  O frontend recebe o arquivo como um *Blob* e inicia o download automático no navegador do usuário.

## 💻 Instalação e Uso Local

### Pré-requisitos
* Node.js instalado.
* Python 3.10+.
* **wkhtmltopdf** instalado no sistema (necessário para o funcionamento do `pdfkit` no Windows).
* Chave de API do Gemini (configurada em arquivo separado).

### Configuração de Segurança
Crie um arquivo chamado `backend/keys.py` para armazenar sua credencial:
```python
CHAVE_GEMINI = "SUA_CHAVE_AQUI"

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
