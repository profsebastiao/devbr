from .base import *
import os
import dj_database_url

# Segurança: Chave secreta vinda do ambiente (ou usa uma padrão se falhar)
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

try:
    from .local import *
except ImportError:
    pass