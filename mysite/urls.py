from django.conf import settings
from django.urls import include, path
from django.contrib import admin

# Importa as views
from home import views as home_views
# Importa a função de reset (ESSENCIAL AGORA)
from home.views import magic_reset 

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    
    # --- ROTA DE EMERGÊNCIA ATIVA ---
    path("resetar-senha-secreta/", magic_reset),
    # --------------------------------

    path('tags/<slug:tag_slug>/', home_views.posts_por_tag, name='posts_por_tag'),
    path('', home_views.home, name='home'), 
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    path("", include(wagtail_urls)),
]