from django.db import models

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=80)
    email = models.EmailField()
    contenido = models.TextField(max_length=400)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.email})"
