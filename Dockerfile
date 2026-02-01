# Usa uma imagem leve do Python 3.12
FROM python:3.12-alpine

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código para dentro do container
COPY . .

# Expõe a porta 5000 (padrão do Flask)
EXPOSE 5000

# Comando para iniciar a aplicação
# Certifique-se que seu arquivo principal se chama app.py. Se for run.py, altere abaixo.
CMD ["python", "app.py"]