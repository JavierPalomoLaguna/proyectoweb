from django.contrib import admin
from .models import MensajeContacto

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha_creacion', 'leido')
    list_filter = ('leido', 'fecha_creacion')
    search_fields = ('nombre', 'email', 'contenido')
    readonly_fields = ('nombre', 'email', 'contenido', 'fecha_creacion')
    
    fieldsets = (
        ('Información del mensaje', {
            'fields': ('nombre', 'email', 'contenido', 'fecha_creacion')
        }),
        ('Estado', {
            'fields': ('leido',)
        }),
    )
    
    def mark_as_read(self, request, queryset):
        queryset.update(leido=True)
    mark_as_read.short_description = "Marcar como leído"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(leido=False)
    mark_as_unread.short_description = "Marcar como no leído"
    
    actions = [mark_as_read, mark_as_unread]
