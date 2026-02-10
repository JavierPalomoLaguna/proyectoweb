from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
    
    def __str__(self):
        return self.nombre
    
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido_espanol = models.TextField()
    contenido_ingles = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='blog/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=False)  # Indica si el post está publicado
    categorias = models.ManyToManyField(Categoria, related_name='posts')
    
    def __str__(self):
        return self.titulo