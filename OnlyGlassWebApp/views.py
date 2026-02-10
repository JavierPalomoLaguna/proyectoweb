from django.shortcuts import render
from contacto.forms import FormularioContacto
from blog.models import Post, Categoria
from .idioma import get_idioma


def home(request):
    # Detectar idioma (URL o sesión)
    lang = get_idioma(request)
    
    # Capturar mensaje de éxito
    mensaje_exito = request.GET.get('mensaje', None)
    
    # Filtrar solo los PUBLICADOS, máximo 6
    posts = Post.objects.filter(publicado=True).prefetch_related('categorias').all()[:6]
    
    # Aplicar idioma a cada post
    for post in posts:
        if lang == 'en':
            post.contenido_mostrar = post.contenido_ingles
        else:
            post.contenido_mostrar = post.contenido_espanol
    
    # Extraer categorías únicas
    categorias_unicas = {}
    for post in posts:
        for cat in post.categorias.all():
            categorias_unicas[cat.nombre] = cat

    context = {
        'posts': posts,
        'categorias_unicas': categorias_unicas.values(),
        'contacto_form': FormularioContacto(),
        'idioma_actual': lang,
        'mensaje_exito': mensaje_exito,  
    }
    return render(request, 'OnlyGlassWebApp/home.html', context)


def politica_cookies(request):
    lang = get_idioma(request)
    context = {
        'title': 'Política de Cookies',
        'meta_description': 'Política de cookies de Only Glass.',
        'idioma_actual': lang,
    }
    return render(request, 'OnlyGlassWebApp/politica_cookies.html', context)


def politica_privacidad(request):
    lang = get_idioma(request)
    context = {
        'title': 'Política de Privacidad',
        'meta_description': 'Política de privacidad de Only Glass.',
        'idioma_actual': lang,
    }
    return render(request, 'OnlyGlassWebApp/politica_privacidad.html', context)


def aviso_legal(request):
    lang = get_idioma(request)
    context = {
        'title': 'Aviso Legal',
        'meta_description': 'Aviso legal de Only Glass.',
        'idioma_actual': lang,
    }
    return render(request, 'OnlyGlassWebApp/aviso_legal.html', context)