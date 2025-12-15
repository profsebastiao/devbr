#!/usr/bin/env bash
# Sair se der erro
set -o errexit

# Instalar dependências
pip install -r requirements.txt

# Converter arquivos estáticos (CSS/Imagens)
python manage.py collectstatic --no-input

# Atualizar o banco de dados
python manage.py migrate