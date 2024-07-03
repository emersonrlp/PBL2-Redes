# Use a imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos necessários para o contêiner
COPY cliente.py .
COPY requirements.txt .

# Defina a variável de ambiente IP
ENV IP_ADDRESS 192.168.1.100

# Instale as dependências (se aplicável)
RUN pip install --no-cache-dir -r requirements.txt

# Defina o comando de inicialização
CMD ["python", "cliente.py"]