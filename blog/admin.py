from django.contrib import admin
from .models import Categoria, Post
from django.utils.safestring import mark_safe
# Register your models here.

class CategoriaAdmin (admin.ModelAdmin):

    readonly_fields = ('created','updated')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'publicado', 'fecha_creacion', 'imagen_preview')
    list_filter = ('publicado', 'categorias', 'fecha_creacion')
    search_fields = ('titulo', 'contenido_espanol', 'contenido_ingles')
    filter_horizontal = ('categorias',)
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'contenido_espanol', 'contenido_ingles')
        }),
        ('Imagen', {
            'fields': ('imagen',)
        }),
        ('Publicación', {
            'fields': ('publicado', 'categorias')
        }),
    )
    def imagen_preview(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" style="max-height: 50px;" />')
        return "Sin imagen"
    imagen_preview.short_description = 'Vista previa'
    
    # Acciones personalizadas
    def marcar_publicados(self, request, queryset):
        queryset.update(publicado=True)
    marcar_publicados.short_description = "Marcar como publicado"
    
    def desmarcar_publicados(self, request, queryset):
        queryset.update(publicado=False)
    desmarcar_publicados.short_description = "Marcar como no publicado"
    
    actions = [marcar_publicados, desmarcar_publicados]

admin.site.register(Categoria, CategoriaAdmin)
