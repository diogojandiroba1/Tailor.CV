FROM node:20-alpine

# Cria a pasta do app no container
WORKDIR /app

# Copia os arquivos de dependência e instala
COPY package.json package-lock.json* ./
RUN npm install

# Copia o resto do código
COPY . .

# Expõe a porta do Next.js
EXPOSE 3000

# Roda em modo de desenvolvimento
CMD ["npm", "run", "dev"]