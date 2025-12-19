from .base import *
import os
import dj_database_url

# Segurança: Chave secreta vinda do ambiente
SECRET_KEY = os.environ.get("SECRET_KEY", "uma-chave-secreta-temporaria-para-build")

# Segurança: Debug deve ser Falso na internet
DEBUG = False

# Permite que o Render acesse o site
ALLOWED_HOSTS = ['*'] 

# Configuração do Banco de Dados (PostgreSQL do Render)
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Configuração de E-mail (Console para não dar erro)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- A CORREÇÃO DO ADMIN VEM AQUI ---
# Obriga o uso do modo "Simples" (Compressed) em vez do "Rigoroso" (Manifest)
# Isso faz o CSS do Wagtail (Admin) voltar a funcionar
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Garante os caminhos corretos
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

try:
    from .local import *
except ImportError:
    pass