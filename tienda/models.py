from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'categoria_producto'
        verbose_name_plural = 'categoria productos'
    
    def __str__(self):
        return self.nombre


class Productos(models.Model):
    nombre = models.CharField(max_length=50)
    caracteristicas = models.CharField(max_length=2500)
    foto_principal = models.ImageField(upload_to='tienda', null=True, blank=True)

    precio_sin_iva = models.DecimalField(max_digits=7, decimal_places=2, default=0,verbose_name="Precio")
    iva_porcentaje = models.DecimalField(max_digits=4, decimal_places=2, default=21.00)

    disponibilidad = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return self.nombre

    @property
    def precio_total(self):
        if self.precio_sin_iva is not None and self.iva_porcentaje is not None:
            return round(self.precio_sin_iva * (1 + self.iva_porcentaje / 100), 2)
        return 0

    @property
    def precio(self):
        # Simula el campo original 'precio' para compatibilidad con el carrito y vistas
        return self.precio_total

    @property
    def iva_desglosado(self):
        # Útil para mostrar el IVA como línea separada en facturas o resúmenes
        return round(self.precio_total - self.precio_sin_iva, 2)

    
class FotoExtraProducto(models.Model):
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='fotos_extra')
    imagen = models.ImageField(upload_to='tienda/fotos_extra', null=True, blank=True)
    descripcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Foto extra de {self.producto.nombre}"

