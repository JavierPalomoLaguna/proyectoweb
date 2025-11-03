from django.contrib import admin
from .models import Cliente
import csv
from django.http import HttpResponse
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin.views.main import ChangeList
# Register your models here.


@admin.action(description="Exportar clientes a CSV")
def exportar_clientes_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=clientes.csv'

    writer = csv.writer(response)
    writer.writerow(['id', 'usuario', 'nombre', 'apellidos', 'telefono', 'email', 'cif',
            'provincia', 'localidad', 'calle', 'numero_calle', 'portal',
            'escalera', 'piso', 'puerta', 'codigo_postal', 'Fecha alta', 'Último cambio'])  # ajusta según tus campos

    for cliente in queryset:
        writer.writerow([
            cliente.id,
            cliente.usuario,
            cliente.nombre,
            cliente.apellidos,
            cliente.telefono,
            cliente.email,
            cliente.cif,
            cliente.provincia,
            cliente.localidad,
            cliente.calle,
            cliente.numero_calle,
            cliente.portal,
            cliente.escalera,
            cliente.piso,
            cliente.puerta,
            cliente.codigo_postal,
            cliente.antiguedad_cliente.strftime('%d/%m/%Y') if cliente.antiguedad_cliente else '',
            cliente.fecha_ultimo_cambio.strftime('%d/%m/%Y') if cliente.fecha_ultimo_cambio else '',
        
        ])

    return response

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'nombre', 'apellidos', 'telefono', 'email', 'cif',
        'provincia', 'localidad', 'calle', 'numero_calle', 'portal',
        'escalera', 'piso', 'puerta', 'codigo_postal','antiguedad_cliente', 'fecha_ultimo_cambio')

    list_filter = ()

    actions = [exportar_clientes_csv]

    # Asocia el changelist personalizado para permitir filtros GET sin redirección ?e=1
    def get_changelist(self, request, **kwargs):
        return ClienteChangeList

    # Aplica filtros personalizados por provincia, localidad, fecha de antigüedad y último cambio
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        provincia = request.GET.get('provincia') or ''
        localidad = request.GET.get('localidad') or ''
        fecha_antiguedad_inicio = request.GET.get('fecha_antiguedad_inicio') or ''
        fecha_antiguedad_fin = request.GET.get('fecha_antiguedad_fin') or ''
        fecha_cambio_inicio = request.GET.get('fecha_cambio_inicio') or ''
        fecha_cambio_fin = request.GET.get('fecha_cambio_fin') or ''

        if provincia.strip():
            qs = qs.filter(provincia__icontains=provincia)
        if localidad.strip():
            qs = qs.filter(localidad__icontains=localidad)

        try:
            if fecha_antiguedad_inicio.strip():
                qs = qs.filter(antiguedad_cliente__gte=fecha_antiguedad_inicio)
            if fecha_antiguedad_fin.strip():
                qs = qs.filter(antiguedad_cliente__lte=fecha_antiguedad_fin)
        except ValueError:
            pass

        try:
            if fecha_cambio_inicio.strip():
                qs = qs.filter(fecha_ultimo_cambio__gte=fecha_cambio_inicio)
            if fecha_cambio_fin.strip():
                qs = qs.filter(fecha_ultimo_cambio__lte=fecha_cambio_fin)
        except ValueError:
            pass

        return qs
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Obtener valores únicos de provincias y localidades
        provincias = self.model.objects.order_by('provincia').values_list('provincia', flat=True).distinct()
        localidades = self.model.objects.order_by('localidad').values_list('localidad', flat=True).distinct()

        extra_context['provincias'] = provincias
        extra_context['localidades'] = localidades

        return super().changelist_view(request, extra_context=extra_context)

# Clase personalizada para permitir filtros GET en el listado de clientes sin redirección ?e=1
class ClienteChangeList(ChangeList):
    def get_filters_params(self, params=None):
        if params is None:
            params = {}
        return {
            k: v for k, v in params.items()
            if k in self.get_filters_config().keys() or k in [
                'provincia', 'localidad', 'fecha_antiguedad_inicio', 'fecha_antiguedad_fin',
                'fecha_cambio_inicio', 'fecha_cambio_fin'
            ]
        }
    
