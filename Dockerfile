# Usa uma imagem oficial do Python baseada no Debian 12 "bookworm"
FROM python:3.12-slim-bookworm

# Adiciona o usuário que será usado no container
RUN useradd wagtail

# Porta usada pelo container
EXPOSE 8000

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Instala pacotes do sistema
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

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

# --- MUDANÇA AQUI ---
# Comentamos esta linha antiga para ela não atrapalhar.
# Vamos deixar o CMD lá embaixo cuidar disso com as senhas reais.
# RUN SECRET_KEY=build-secret-key python manage.py collectstatic --noinput --clear

# Comando Mestre que roda quando o site inicia (Runtime):
# 1. Gera o CSS (collectstatic)
# 2. Atualiza Banco (migrate)
# 3. Inicia Site (gunicorn)
CMD python manage.py collectstatic --noinput; python manage.py migrate --noinput; gunicorn mysite.wsgi:application --bind 0.0.0.0:8000