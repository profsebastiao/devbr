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

# Configuração de E-mail
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- CORREÇÃO DEFINITIVA DO CSS ---
# 1. Usa o modo simples do Whitenoise (Funciona sempre)
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# 2. Garante que a pasta seja A MESMA do base.py ('static')
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # <--- Aqui estava 'staticfiles', voltei para 'static'

try:
    from .local import *
except ImportError:
    pass