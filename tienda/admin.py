from django.contrib import admin, messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.admin.views.main import ChangeList
from django import forms
from django.http import HttpResponse
from django.urls import path
from .models import Productos, CategoriaProducto, FotoExtraProducto
from decimal import Decimal, InvalidOperation
import csv
# Importaciones necesarias para el admin, formularios, envío de correos, manejo de URLs, modelos y CSV.


# Formulario útil si usas la vista exportar_csv (con filtros manuales y selección de productos)
# Si decides eliminar esa vista, este formulario también puede eliminarse
class ExportarCSVForm(forms.Form):
    fecha_inicio = forms.DateField(required=False, label="Desde fecha")
    fecha_fin = forms.DateField(required=False, label="Hasta fecha")
    categoria = forms.ModelChoiceField(
        queryset=CategoriaProducto.objects.all(),
        required=False,
        label="Categoría"
    )
    productos = forms.ModelMultipleChoiceField(
        queryset=Productos.objects.all(),
        required=False,
        label="Productos específicos"
    )
    
# Inline funcional para mostrar fotos adicionales en el admin de productos
# Se usa en ProductoAdmin.inlines
class FotoExtraInline(admin.TabularInline):
    model = FotoExtraProducto
    extra = 1
    fields = ('imagen', 'descripcion')
    readonly_fields = ('id',)

# Clase esencial para evitar ?e=1 y permitir filtros personalizados
# Conserva los filtros nativos (list_filter) y permite los tuyos (precio_min, stock_max, etc.)
class CustomChangeList(ChangeList):
    def get_filters_params(self, params=None):
        if params is None:
            params = {}
        return {
            k: v for k, v in params.items()
            if k in self.get_filters_config().keys() or k in [
                'precio_min', 'precio_max', 'stock_min', 'stock_max',
                'fecha_inicio', 'fecha_fin', 'categoria'
            ]
        }

def exportar_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=productos_filtrados.csv'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Stock', 'Precio', 'Categoría', 'Fecha creación'])

    for p in queryset:
        writer.writerow([
            p.id,
            p.nombre,
            p.stock,
            p.precio_total,
            p.categoria.nombre if p.categoria else '',
            p.created.strftime('%Y-%m-%d %H:%M')
        ])

    return response

exportar_csv.short_description = "Exportar productos filtrados a CSV"



# Configuración principal del modelo Productos en el panel de administración.
# Define campos visibles, filtros, inlines y lógica de filtrado personalizada.
class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    inlines = [FotoExtraInline]

    list_display = (
        'nombre', 'precio_sin_iva', 'iva_porcentaje', 'precio_total',
        'disponibilidad', 'stock', 'categoria', 'created'
    )

    list_filter = ['disponibilidad']

    fields = (
        'nombre', 'caracteristicas', 'foto_principal',
        'precio_sin_iva', 'iva_porcentaje',
        'disponibilidad', 'stock', 'categoria',
        'created', 'updated'
    )
    actions = [exportar_csv]

    # Aplica filtros personalizados al queryset según los parámetros GET recibidos.
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        precio_min = request.GET.get('precio_min') or ''
        precio_max = request.GET.get('precio_max') or ''
        stock_min = request.GET.get('stock_min') or ''
        stock_max = request.GET.get('stock_max') or ''
        fecha_inicio = request.GET.get('fecha_inicio') or ''
        fecha_fin = request.GET.get('fecha_fin') or ''
        categoria_id = request.GET.get('categoria') or ''

        # Precio
        try:
            if precio_min.strip():
                qs = qs.filter(precio_sin_iva__gte=Decimal(precio_min))
            if precio_max.strip():
                qs = qs.filter(precio_sin_iva__lte=Decimal(precio_max))
        except (InvalidOperation, ValueError):
            pass

        # Stock
        try:
            if stock_min.strip():
                qs = qs.filter(stock__gte=int(stock_min))
            if stock_max.strip():
                qs = qs.filter(stock__lte=int(stock_max))
        except ValueError:
            pass

        # Fecha
        try:
            if fecha_inicio.strip():
                qs = qs.filter(created__date__gte=fecha_inicio)
            if fecha_fin.strip():
                qs = qs.filter(created__date__lte=fecha_fin)
        except ValueError:
            pass

        # Categoría
        try:
            if categoria_id.strip():
                qs = qs.filter(categoria_id=int(categoria_id))
        except ValueError:
            pass

        # Disponibilidad (filtro nativo)
        disponibilidad = request.GET.get('disponibilidad__exact')
        if disponibilidad in ['0', '1']:
            qs = qs.filter(disponibilidad=bool(int(disponibilidad)))

        return qs

    # Vista personalizada del listado en el admin.
    # Elimina el parámetro ?e=1, lanza alerta de stock bajo y envía correos si hay productos con menos de 10 unidades.
    # También inyecta las categorías en el contexto para usarlas en el template.
    def changelist_view(self, request, extra_context=None):

        request.GET._mutable = True
        if 'e' in request.GET:
            del request.GET['e']            
        request.GET._mutable = False

        # --- Alerta de stock bajo ---
        bajos = Productos.objects.filter(stock__lt=10)
        if bajos.exists():
            nombres = ', '.join([p.nombre for p in bajos])
            messages.warning(request, f"⚠️ Stock bajo en: {nombres}")

            usuarios_con_permiso = User.objects.filter(
                is_active=True,
                is_staff=True,
                user_permissions__codename__in=[
                    'view_productos', 'change_productos', 'delete_productos', 'add_productos'
                ]
            ).distinct()

            usuarios_por_grupo = User.objects.filter(
                is_active=True,
                is_staff=True,
                groups__permissions__codename__in=[
                    'view_productos', 'change_productos', 'delete_productos', 'add_productos'
                ]
            ).distinct()

            destinatarios = set(
                u.email for u in list(usuarios_con_permiso) + list(usuarios_por_grupo)
                if u.email
            )

            if destinatarios:
                send_mail(
                    subject='⚠️ Alerta de stock bajo',
                    message=f"Los siguientes productos tienen menos de 10 unidades en stock:\n\n{nombres}",
                    from_email='notificaciones@tusistema.com',
                    recipient_list=list(destinatarios),
                    fail_silently=True
                )

        # --- Inicializar extra_context si es None ---
        if extra_context is None:
            extra_context = {}

        # --- Inyectar categorías para el select ---
        extra_context['categorias'] = CategoriaProducto.objects.all()

        return super().changelist_view(request, extra_context=extra_context)
    
    
    def get_changelist(self, request, **kwargs):
        return CustomChangeList
    


# Configuración básica del modelo CategoriaProducto en el panel de administración.
# Solo se marcan como de solo lectura los campos de fecha.    
class CategoriaProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    
# Registro de los modelos en el panel de administración con sus respectivas configuraciones.
admin.site.register(Productos, ProductoAdmin)
admin.site.register(CategoriaProducto, CategoriaProductoAdmin)
