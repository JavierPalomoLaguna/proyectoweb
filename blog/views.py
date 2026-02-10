import unicodedata
import re
from django.http import Http404
from blog.models import Post, Categoria
from django.shortcuts import render, get_object_or_404
from OnlyGlassWebApp.idioma import get_idioma


def blog(request):
    lang = get_idioma(request)
    posts = Post.objects.prefetch_related('categorias').all()

    # Aplicar idioma a cada post
    for post in posts:
        if lang == 'en':
            post.contenido_mostrar = post.contenido_ingles
        else:
            post.contenido_mostrar = post.contenido_espanol

    # Extraer objetos únicos de categoría por nombre
    categorias_unicas = {}
    for post in posts:
        for cat in post.categorias.all():
            categorias_unicas[cat.nombre] = cat

    context = {
        'posts': posts,
        'categorias_unicas': categorias_unicas.values(),
        'idioma_actual': lang,
        'meta_title': 'Poner datos sobre cristaleria',
        'meta_description': 'SEO para cristaleria.',
    }
    return render(request, 'blog/blog.html', context)


def normalizar(texto):
    """Convierte a minúsculas, quita tildes y elimina caracteres especiales"""
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9]+', '', texto)
    return texto


def categoria(request, nombre_categoria):
    lang = get_idioma(request)
    post_id_destacado = request.GET.get('post_id', None)
    
    # Caso especial: mostrar todos los posts
    if nombre_categoria.lower() == 'todos':
        categoria = None
        posts = Post.objects.all()
    else:
        # Buscar categoría comparando versiones normalizadas
        nombre_normalizado = normalizar(nombre_categoria)
        categoria = None
        for cat in Categoria.objects.all():
            if normalizar(cat.nombre) == nombre_normalizado:
                categoria = cat
                break
        
        if not categoria:
            raise Http404("Categoría no encontrada")
        
        posts = Post.objects.filter(categorias=categoria)
    
    for post in posts:
        if lang == 'en':
            post.contenido_mostrar = post.contenido_ingles
        else:
            post.contenido_mostrar = post.contenido_espanol
        
        if post_id_destacado and str(post.id) == post_id_destacado:
            post.destacado = True
        else:
            post.destacado = False
    
    todas_categorias = Categoria.objects.all()
    context = {
        "categoria": categoria,
        "posts": posts,
        "idioma_actual": lang,
        "post_id_destacado": post_id_destacado,
        "categorias_unicas": todas_categorias,
        "mostrar_todos": nombre_categoria.lower() == 'todos',
    }
    return render(request, "blog/categoria.html", context)