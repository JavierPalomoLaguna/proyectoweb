from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .carro import Carro
from tienda.models import Productos
from django.conf import settings

def ver_carro(request):
    carro_instancia = Carro(request)
    datos_carro = request.session.get("carro", {})
    
    # Calcular totales
    for item in datos_carro.values():
        item["total"] = item["precio"] * item["cantidad"]

    return render(request, 'carro/carro.html', {
        'carro': datos_carro,
        'productos_total_carro': carro_instancia.total_carro(),
        'importe_total_carro': carro_instancia.total_importe(),
    })

def agregar_producto(request, producto_id):
    carro = Carro(request)
    producto = get_object_or_404(Productos, id=producto_id)

    # Guardar la categoría del producto en la sesión para redirigir luego
    request.session["ultima_categoria"] = producto.categoria.id

    producto_id_str = str(producto.id)
    cantidad_actual = carro.carro.get(producto_id_str, {}).get("cantidad", 0)

    if cantidad_actual < producto.stock:
        carro.agregar(producto=producto)
        return redirect('tienda')
    else:
        request.session["limite_stock"] = producto.id
        return redirect('stock_extendido', producto_id=producto.id)

def sumar_producto(request, producto_id):
    carro = Carro(request)
    producto = get_object_or_404(Productos, id=producto_id)

    producto_id_str = str(producto.id)
    cantidad_actual = carro.carro.get(producto_id_str, {}).get("cantidad", 0)

    if cantidad_actual < producto.stock:
        carro.agregar(producto=producto)
        return redirect('ver_carro')
    else:
        request.session["limite_stock"] = producto.id
        return redirect('stock_extendido', producto_id=producto.id)
    
def restar_producto(request, producto_id):
    carro = Carro(request)
    producto = get_object_or_404(Productos, id=producto_id)
    carro.restar(producto=producto)
    return redirect('ver_carro')

def eliminar_producto(request, producto_id):
    carro = Carro(request)
    producto = get_object_or_404(Productos, id=producto_id)
    carro.eliminar(producto=producto)
    return redirect('ver_carro')

def vaciar_carro(request):
    carro = Carro(request)
    carro.limpiar_carro()
    return redirect('tienda')

def stock_extendido(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)
    carro = Carro(request)
    cantidad_actual = carro.carro.get(str(producto.id), {}).get("cantidad", 0)
    return render(request, 'carro/stock_extendido.html', {
        'producto': producto,
        'cantidad_actual': cantidad_actual,
        'stock_disponible': producto.stock
    })

@require_POST
def ajustar_stock(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)
    carro = Carro(request)
    producto_id_str = str(producto.id)
    if producto_id_str in carro.carro:
        carro.carro[producto_id_str]["cantidad"] = producto.stock
        carro.guardar_carro()
    request.session.pop("limite_stock", None)
    return redirect('ver_carro')

@login_required(login_url='login')
def tramitar_pedido(request):
    carro = Carro(request)
    datos_carro = request.session.get("carro", {})
    return render(request, 'carro/tramitar_pedido.html', {
        'carro': datos_carro,
        'productos_total_carro': carro.total_carro(),
        'importe_total_carro': carro.total_importe()
    })
