# Tailor.CV 📄⚡

Um utilitário alimentado por IA para otimizar, adequar e gerar currículos profissionais prontos para envio, com base em descrições de vagas específicas. O Tailor.CV ajuda candidatos a passarem pelos filtros de ATS (Applicant Tracking Systems) ajustando o conteúdo e formatando o resultado em templates aceitos pelo mercado.

## 🚀 Funcionalidades

O sistema possui fluxos de análise, otimização e formatação:

### 1. Modos de Operação
* **🔍 Analisador de Gaps (Gap Analyzer):** Compara o currículo atual com a vaga e gera um relatório estratégico do que está faltando. Sugere tópicos de estudo ou como aproveitar projetos acadêmicos e pessoais para preencher essas lacunas.
* **🛡️ Otimização Segura:** Reescreve as experiências *existentes* no currículo usando as palavras-chave da vaga, sem inventar nenhuma habilidade que o candidato não possua.
* **⚠️ Modo Inclusão:** Injeta as palavras-chave e habilidades exigidas pela vaga diretamente no currículo, mesclando-as com as experiências do usuário, independentemente de ele possuir a habilidade ou não.

### 2. Formatação e Exportação
* **🎨 Template Recomendado:** Utiliza um template construído em LaTeX focado em clareza, tipografia profissional e estrutura **ATS-Friendly** (fácil de ler por sistemas automatizados de recrutamento).
* **📥 Exportação Direta para PDF:** O sistema gera o currículo nativamente em PDF de alta qualidade e inicia o download imediato.

## 🛠️ Tecnologias Utilizadas

* **Frontend:** React, Next.js, Tailwind CSS.
* **Backend:** Python, FastAPI.
* **Manipulação e Leitura de PDF:** `pdfplumber` (para extrair texto do CV original).
* **Inteligência Artificial:** Google Gemini API (via SDK `google-genai`, utilizando o modelo `gemini-2.5-flash`).
* **Geração de PDF:** `Jinja2` (para injeção de dados no template) e compilação nativa de **LaTeX** (via `subprocess` chamando `pdflatex`).

## ⚙️ Como Funciona

1.  O usuário faz o upload do seu currículo em `.pdf` e cola a descrição da vaga na interface.
2.  Seleciona o modo de operação da IA.
3.  O backend extrai o texto do PDF original e envia para o modelo Gemini com um prompt estruturado para retorno em JSON.
4.  O LLM retorna o conteúdo analisado ou otimizado (Resumo, Experiências, Habilidades, etc.).
5.  O backend aplica esses dados em um template `.tex` usando variáveis adaptadas do **Jinja2**.
6.  O sistema executa o compilador LaTeX da máquina para gerar o arquivo final.
7.  O frontend recebe o binário final e força o download no navegador.

## 💻 Instalação e Uso Local

### Pré-requisitos
* Node.js instalado.
* Python 3.10+.
* **MiKTeX** (Windows) ou **TeX Live** (Linux/Mac) instalado e configurado nas variáveis de ambiente (necessário para o comando `pdflatex`).

### Configuração de Segurança
Crie um arquivo chamado `keys.py` na raiz da pasta `backend` para armazenar sua credencial:
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
-[ ] Sistema de Créditos e Monetização (SaaS): Implementar modelo de uso onde o "Gap Analyzer" funciona como ferramenta gratuita (entregando apenas o relatório de análise) e a geração/otimização real do PDF do currículo é restrita a usuários pagantes ou com saldo de créditos.
-[ ] Extensão para navegador que lê a vaga do LinkedIn e preenche os dados automaticamente.
-[ ] Histórico de currículos gerados por usuário (com sistema de autenticação).
