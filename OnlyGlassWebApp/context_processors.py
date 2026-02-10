from .idioma import get_idioma, get_traducciones
from blog.models import Categoria


def datos_globales(request):
    """Context processor para datos disponibles en todas las plantillas"""
    lang = get_idioma(request)
    return {
        'idioma_actual': lang,
        't': get_traducciones(lang),
        'categorias_unicas': Categoria.objects.all(),
    }