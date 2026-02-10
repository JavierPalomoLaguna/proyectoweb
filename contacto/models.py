from django.db import models

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)  # ← Añade este campo
    
    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"
        ordering = ['-fecha_creacion']  # Más recientes primero