from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag 
from .models import BlogPage 

def home(request):
    # 1. Pega TODOS os posts (QuerySet)
    all_posts = BlogPage.objects.live().order_by('-date')
    
    # 2. CONFIGURA A PAGINAÇÃO
    # O número '3' define quantos posts aparecem por vez.
    paginator = Paginator(all_posts, 3) 
    
    # 3. Descobre qual página o usuário quer ver (1, 2, 3...)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Se não tiver número na URL, mostra a primeira página
        posts = paginator.page(1)
    except EmptyPage:
        # Se o número for inválido (ex: 999), mostra a última
        posts = paginator.page(paginator.num_pages)

    # 4. Manda apenas os 3 posts da vez para o HTML
    return render(request, 'home/home_page.html', {'posts': posts})

def posts_por_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    
    # Filtra posts pela tag
    all_posts = BlogPage.objects.live().filter(tags__in=[tag]).order_by('-date')
    
    # Paginação para as tags também
    paginator = Paginator(all_posts, 3) 
    
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'home/home_page.html', {'posts': posts, 'tag': tag})