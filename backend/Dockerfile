FROM python:3.12-slim

# Instala o LaTeX, pacotes extras e o cm-super
RUN apt-get update && \
    apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-latex-extra cm-super && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# cria pasta app no container
WORKDIR /app 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]