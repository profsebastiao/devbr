# Usa uma imagem oficial do Python baseada no Debian 12 "bookworm"
FROM python:3.12-slim-bookworm

# Adiciona o usuário que será usado no container
RUN useradd wagtail

# Porta usada pelo container
EXPOSE 8000

# Define variáveis de ambiente
# PYTHONUNBUFFERED: Garante que os logs apareçam imediatamente no painel do Render
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Instala pacotes do sistema necessários para Wagtail, Django e Postgres
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

# (REMOVIDO: A instalação manual do Gunicorn antigo. Deixamos o requirements.txt cuidar disso)

# Instala os requerimentos do projeto
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Define a pasta de trabalho
WORKDIR /app

# Define as permissões da pasta para o usuário wagtail
RUN chown wagtail:wagtail /app

# Copia o código fonte para dentro do container
COPY --chown=wagtail:wagtail . .

# Troca para o usuário wagtail (segurança)
USER wagtail

# Coleta os arquivos estáticos (CSS/JS)
# TRUQUE: Passamos uma SECRET_KEY falsa aqui só para o comando não falhar durante o build
RUN SECRET_KEY=build-secret-key python manage.py collectstatic --noinput --clear

# Comando que roda quando o site inicia
# 1. Roda as migrações do banco
# 2. Inicia o Gunicorn ligando no IP 0.0.0.0 (Essencial para o Render)
CMD set -xe; python manage.py migrate --noinput; gunicorn mysite.wsgi:application --bind 0.0.0.0:8000