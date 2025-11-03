from django.urls import path
from . import views

# app_name = "carro"  # Si se activa, todas las URLs de esta app deben llamarse con prefijo: 'carro:...'
#                     # Útil si se usa include() con namespace en urls.py principal o si hay conflictos de nombres.
#                     # Si no se usa espacio de nombres, dejar comentado para evitar errores tipo NoReverseMatch.

urlpatterns = [
    path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar_producto'),
    # Para que en el futuro sea más legible duplico con un alias "agregar_al_carro"
    # path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar_al_carro'),
    path('sumar/<int:producto_id>/', views.sumar_producto, name='sumar_producto'),
    path('restar/<int:producto_id>/', views.restar_producto, name='restar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('vaciar/', views.vaciar_carro, name='vaciar_carro'),
    path('', views.ver_carro, name='ver_carro'),

    # nuevas rutas de control de stock
    path('stock_extendido/<int:producto_id>/', views.stock_extendido, name='stock_extendido'),
    path('ajustar_stock/<int:producto_id>/', views.ajustar_stock, name='ajustar_stock'),
]