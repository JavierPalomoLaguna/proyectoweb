from django.contrib import admin
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from .models import Pedido, LineaPedido, ConfiguracionEnvio

class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'subtotal')
    can_delete = False

@admin.register(ConfiguracionEnvio)
class ConfiguracionEnvioAdmin(admin.ModelAdmin):
    list_display = ('umbral_envio_gratis', 'costo_envio_estandar', 'activo')
    list_editable = ('activo',)
    
    def has_add_permission(self, request):
        # Permitir agregar solo si no existe ninguna configuración
        if ConfiguracionEnvio.objects.exists():
            return False
        return True

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'cliente', 
        'fecha', 
        'pagado', 
        'metodo_pago',
        'enviado',
        'gastos_envio',  
        'envio_gratis',  
        'get_factura_link',  # ✅ NUEVO: Enlace a factura
        'codigo_autorizacion', 
        'codigo_respuesta',      
        'descripcion_error',     
        'fecha_pago', 
        'hora_pago', 
        'get_total'
    )
    list_filter = (
        'pagado',
        'enviado',
        'envio_gratis',  
        'metodo_pago',
        ('fecha', admin.DateFieldListFilter),
        ('fecha_pago', admin.DateFieldListFilter),
        'pais_tarjeta',
    )
    search_fields = (
        'cliente__nombre', 
        'id', 
        'codigo_autorizacion',
        'codigo_respuesta',      
        'descripcion_error'      
    )
    readonly_fields = ('fecha_envio',)
    date_hierarchy = 'fecha'
    ordering = ('-fecha',)
    inlines = [LineaPedidoInline]
    
    actions = ['marcar_como_enviado']
    
    def marcar_como_enviado(self, request, queryset):
        updated = queryset.update(enviado=True, fecha_envio=timezone.now())
        self.message_user(request, f"{updated} pedido(s) marcado(s) como enviado(s)")
    marcar_como_enviado.short_description = "Marcar pedidos seleccionados como enviados"
    
    # ✅ NUEVO: MÉTODO PARA ENLACE A FACTURA
    def get_factura_link(self, obj):
        if obj.pagado:  # Solo mostrar enlace si está pagado
            return format_html('<a href="{}" target="_blank">📄 Ver Factura #{}</a>', 
                             reverse('ver_factura', args=[obj.id]), obj.id)
        return "❌ Pendiente pago"
    get_factura_link.short_description = 'Factura'
    get_factura_link.allow_tags = True
    
    def get_total(self, obj):
        return f"{obj.total:.2f} €" if obj.total else "0.00 €"
    get_total.short_description = 'Total'

@admin.register(LineaPedido)
class LineaPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'producto', 'cantidad', 'subtotal')
    search_fields = ('pedido__id', 'producto__nombre')
    readonly_fields = ('subtotal',)