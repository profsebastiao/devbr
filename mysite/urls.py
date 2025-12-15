from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from home import views as home_views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),

    # --- NOVA ROTA PARA AS TAGS (ADICIONADA AQUI) ---
    # Explicação: O <slug:tag_slug> é como uma "variável". 
    # Se a URL for /tags/python/, o Django entende que "python" é o tag_slug.
    path('tags/<slug:tag_slug>/', home_views.posts_por_tag, name='posts_por_tag'),
    # ------------------------------------------------

    # Sua rota personalizada da Home
    path('', home_views.home, name='home'), 
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # Esta é a regra oficial do Wagtail que captura tudo que não foi definido acima.
    path("", include(wagtail_urls)),
]