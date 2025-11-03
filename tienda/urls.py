from django.urls import path
from django.contrib import admin
from . import views
from tienda.views import exportar_csv

urlpatterns = [
    path('', views.tienda, name='tienda'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('checkout/', views.checkout, name='checkout'),
    path("admin/exportar_csv/", admin.site.admin_view(exportar_csv), name="exportar_csv"),  # ✅ única ruta para CSV
]