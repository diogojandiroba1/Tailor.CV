# Tailor.CV 📄⚡

Um utilitário SaaS alimentado por IA para otimizar, adequar e gerar currículos profissionais prontos para envio, com base em descrições de vagas específicas. O Tailor.CV ajuda candidatos a passarem pelos filtros de ATS (Applicant Tracking Systems) ajustando o conteúdo, injetando o método STAR e formatando o resultado em templates em LaTeX aceitos pelo mercado.

## 🚀 Funcionalidades

O sistema possui fluxos completos de análise, personalização, otimização e formatação:

### 1. Autenticação e Gestão (SaaS)
* **🔐 Login e Dashboard:** Sistema de autenticação moderno e seguro. Usuários logados possuem um painel próprio para gerenciar seus dados e, futuramente, seus créditos e histórico de currículos.

### 2. Modos de Operação (IA)
* **🔍 Analisador de Gaps (Gap Analyzer):** Compara o currículo atual com a vaga e gera um **relatório executivo em PDF** listando o seu *Match Score*, lacunas críticas e um plano de ação realista do que estudar até a entrevista.
* **🛡️ Otimização Segura:** Reescreve as experiências *existentes* no currículo usando jargões e palavras-chave da vaga. Aplica o método STAR (Situação, Tarefa, Ação, Resultado) sem inventar anos de experiência falsos.
* **⚠️ Modo Full Match (Inclusão):** Injeta as ferramentas e requisitos da vaga diretamente nas experiências passadas do usuário de forma agressiva, criando um currículo moldado para burlar filtros engessados de ATS.

### 3. Personalização Modular
* **⚙️ Currículo "Lego":** O usuário tem o poder de ligar e desligar seções do currículo (Resumo Profissional, Experiência, Cursos e Liderança/Projetos). A IA e o template se adaptam dinamicamente para gerar apenas o que foi solicitado, economizando tokens e tempo.

### 4. Formatação e Exportação
* **🎨 Template Recomendado:** Utiliza templates construídos em **LaTeX** focados em clareza, tipografia e estrutura 100% **ATS-Friendly**.
* **📥 Exportação Direta:** O sistema compila o código nativamente no servidor e força o download imediato do PDF de alta qualidade no navegador.

## 🛠️ Tecnologias Utilizadas

* **Frontend:** React, Next.js (Turbopack), Tailwind CSS, Lucide-react (Ícones).
* **Autenticação:** Clerk.
* **Backend:** Python, FastAPI.
* **Manipulação e Leitura de PDF:** `pdfplumber` (extração de texto).
* **Inteligência Artificial:** Google Gemini API (via SDK `google-genai`, modelo `gemini-2.5-flash`).
* **Geração de PDF:** `Jinja2` (injeção dinâmica de dados) e compilação nativa de **LaTeX** (via subprocesso `pdflatex`).

## ⚙️ Como Funciona

1. O usuário cria uma conta ou faz login para acessar o gerador.
2. Faz o upload do currículo original (`.pdf`) e cola a descrição da vaga desejada.
3. Escolhe o Modo de IA (Gaps, Seguro ou Full Match) e **personaliza quais seções** deseja incluir no documento final.
4. O backend extrai o texto e monta um prompt dinâmico, exigindo um retorno estrito em JSON.
5. O LLM aplica as regras de reescrita (sem jargões de IA, focando em fatos e métricas).
6. O backend injeta o JSON retornado em um template `.tex` usando o Jinja2.
7. O servidor executa o compilador LaTeX da máquina para gerar o PDF e o devolve para o frontend.

## 💻 Instalação e Uso Local

### Pré-requisitos
* Node.js instalado.
* Python 3.10+.
* **MiKTeX** (Windows) ou **TeX Live** (Linux/Mac) configurado nas variáveis de ambiente.
* Instalar o pacote `cm-super` no MiKTeX (caso use Windows).

### Configuração do Backend (FastAPI)
1. Crie um arquivo `keys.py` na raiz da pasta `backend`:
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

1. Crie uma conta no Clerk e um novo projeto.
2. Crie um arquivo .env.local na raiz da pasta frontend com as suas chaves:

\`\`\`bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_sua_chave_aqui
CLERK_SECRET_KEY=sk_test_sua_chave_secreta_aqui
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
\`\`\`
Por fim, 
\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

## 📝 Próximos Passos / Melhorias Futuras
[x] Histórico de currículos gerados por usuário e sistema de autenticação.
[ ] Sistema de Créditos e Monetização (SaaS) com Banco de Dados: Implementar modelo Freemium onde o "Gap Analyzer" gasta 0 créditos e a geração de currículos otimizados consome saldo pago (integração via Stripe/Mercado Pago).
[ ] Editor Web de LaTeX integrado para ajustes finos manuais antes de baixar o PDF.
[ ] Extensão para navegador ou Web Scraper interno (BeautifulSoup) para extrair os dados da vaga direto de links da Gupy/LinkedIn.
