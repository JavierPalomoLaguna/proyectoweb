from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('tramitar/', views.tramitar_pedido, name='tramitar_pedido'),
    path('pedido_confirmado/', views.pedido_confirmado, name='pedido_confirmado'),
    path('reset/<str:token>/', views.reset_password, name='reset_password'),
    path('solicitar-reset/', views.solicitar_reset, name='solicitar_reset'),
    path('logout/', views.logout_cliente, name='logout_cliente'),
    path('zona/', views.zona_cliente, name='zona_cliente'),
    path('confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
    path('zona/editar/', views.editar_datos_cliente, name='editar_datos_cliente'),
    path('zona/historial/', views.historial_pedidos, name='historial_pedidos'),
    path('zona/pedidos/', views.historial_pedidos, name='ver_pedidos_cliente'),
    path('admin/clientes/localidades/', views.localidades_por_provincia, name='localidades_por_provincia'),
    path('zona/pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]
