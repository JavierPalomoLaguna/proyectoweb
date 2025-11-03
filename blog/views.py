from django.shortcuts import render
from blog.models import Post, Categoria

# Create your views here.

def blog(request):
    posts = Post.objects.prefetch_related('categorias').all()

    # Extraer objetos únicos de categoría por nombre
    categorias_unicas = {}
    for post in posts:
        for cat in post.categorias.all():
            categorias_unicas[cat.nombre] = cat  # sobrescribe duplicados por nombre

    return render(request, 'blog/blog.html', {
        'posts': posts,
        'categorias_unicas': categorias_unicas.values(),  # lista de objetos únicos
    })

def categoria(request, categoria_id):

    categoria = Categoria.objects.get(id=categoria_id)
    posts = Post.objects.filter(categorias= categoria)
    return render(request, "blog/categoria.html", {"categoria": categoria, "posts":posts})
