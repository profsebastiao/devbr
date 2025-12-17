from django.conf import settings
from django.urls import include, path
from django.contrib import admin

# Importa as views (telas) do seu app 'home'
from home import views as home_views
# Importa especificamente a função de resetar senha
from home.views import magic_reset 

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

urlpatterns = [
    # Painel administrativo padrão do Django (pouco usado no Wagtail)
    path("django-admin/", admin.site.urls),

    # Painel administrativo do Wagtail (onde você edita os posts)
    path("admin/", include(wagtailadmin_urls)),

    # Gerenciamento de documentos (PDFs, etc)
    path("documents/", include(wagtaildocs_urls)),

    # Página de busca
    path("search/", search_views.search, name="search"),
    
    # --- ROTA MÁGICA DE EMERGÊNCIA ---
    # Ao acessar site.com/resetar-senha-secreta/, a senha do admin vira 123456
    path("resetar-senha-secreta/", magic_reset),
    # ---------------------------------

    # --- ROTA PARA AS TAGS ---
    # Exemplo: /tags/python/ chama a função posts_por_tag
    path('tags/<slug:tag_slug>/', home_views.posts_por_tag, name='posts_por_tag'),

    # --- ROTA DA HOME PAGE ---
    # Força o Django a usar a sua 'view' personalizada para a página inicial
    path('', home_views.home, name='home'), 
]


# Configurações para servir imagens no computador local (Debug)
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# --- ROTA PEGA-TUDO DO WAGTAIL ---
# Qualquer link que não foi achado acima (ex: /sobre-mim/, /contato/)
# cai aqui e o Wagtail tenta encontrar a página no banco de dados.
urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]