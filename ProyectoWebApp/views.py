from django.shortcuts import render
from django.db.models import Subquery, OuterRef
from tienda.models import Productos, CategoriaProducto


# Create your views here.
def home(request):
    categorias = CategoriaProducto.objects.all()[:5]  # Limita a 5 categorías
    productos_por_categoria = []

    for categoria in categorias:
        producto = Productos.objects.filter(categoria=categoria, disponibilidad=True).first()
        if producto:
            productos_por_categoria.append(producto)

    return render(request, 'ProyectoWebApp/index.html', {
        'productos_por_categoria': productos_por_categoria
    })


def politica_cookies(request):
    context = {
        'title': 'Política de Cookies',
        'meta_description': 'Política de cookies de Código Vivo Studio.'
    }
    return render(request, 'ProyectoWebApp/politica_cookies.html', context)

def politica_privacidad(request):
    context = {
        'title': 'Política de Privacidad',
        'meta_description': 'Política de privacidad de Código Vivo Studio. Información sobre protección de datos personales.'
    }
    return render(request, 'ProyectoWebApp/politica_privacidad.html', context)

def aviso_legal(request):
    context = {
        'title': 'Aviso Legal',
        'meta_description': 'Aviso legal de Código Vivo Studio. Condiciones de uso del sitio web y información legal.'
    }
    return render(request, 'ProyectoWebApp/aviso_legal.html', context)