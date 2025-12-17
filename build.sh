#!/usr/bin/env bash
# Sair se der erro
set -o errexit

# Instalar tudo
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

# --- O PULO DO GATO (CRIAR ADMIN) ---
# Este comando verifica se o 'admin' existe. Se não existir, cria com a senha '123456'
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@exemplo.com', '123456')"
