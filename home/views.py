from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag 
from .models import BlogPage 

def home(request):
    # --- RASTREADOR (Vai aparecer no seu terminal preto) ---
    print("--------------------------------------------------")
    print("ALERTA: O NOVO SISTEMA DE PAGINAÇÃO FOI ACIONADO!")
    print("--------------------------------------------------")
    # -------------------------------------------------------

    # 1. Pega todos os posts
    all_posts = BlogPage.objects.live().order_by('-date')
    
    # 2. Define que só pode mostrar 10 por vez
    paginator = Paginator(all_posts, 10) 
    
    # 3. Verifica qual página o usuário pediu
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # 4. Manda a lista fatiada (só 3 posts) para o site
    return render(request, 'home/home_page.html', {'posts': posts})

def posts_por_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    all_posts = BlogPage.objects.live().filter(tags__in=[tag]).order_by('-date')
    
    paginator = Paginator(all_posts, 10) 
    
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'home/home_page.html', {'posts': posts, 'tag': tag})