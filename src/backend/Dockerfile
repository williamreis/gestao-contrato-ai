# Dockerfile para Contrato AI Backend (FastAPI)
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
# Usamos --no-cache-dir para evitar o cache do pip, reduzindo o tamanho da imagem
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expõe as portas das APIs
EXPOSE 8000 8001
