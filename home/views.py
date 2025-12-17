from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag 
from .models import BlogPage 

def home(request):
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

    # 4. Manda a lista fatiada para o site
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

# --- FUNÇÃO DE EMERGÊNCIA PARA O RENDER ---
def magic_reset(request):
    # Tenta pegar o usuário 'admin', ou cria se não existir
    user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@exemplo.com'})
    
    # Define a senha à força para 123456
    user.set_password('123456')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    
    return HttpResponse("<h1>SUCESSO! 🔓</h1><p>A senha do usuário <b>admin</b> foi resetada para <b>123456</b>.<br><a href='/admin/'>Clique aqui para entrar</a></p>")