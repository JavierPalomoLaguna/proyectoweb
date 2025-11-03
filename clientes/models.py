from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets

# Create your models here.



class Cliente(models.Model):
    usuario = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=12)
    email = models.EmailField()  # mejor que sea único unique=True
    cif = models.CharField(max_length=20, null=True, blank=True)
    provincia = models.CharField(max_length=30)
    localidad = models.CharField(max_length=100)
    calle = models.CharField(max_length=150)
    numero_calle = models.CharField(max_length=3)
    portal = models.CharField(max_length=3, blank=True)
    escalera = models.CharField(max_length=3, blank=True)
    piso = models.CharField(max_length=3)
    puerta = models.CharField(max_length=3)
    codigo_postal = models.CharField(max_length=5)
    antiguedad_cliente = models.DateTimeField(auto_now_add=True)
    fecha_ultimo_cambio = models.DateTimeField(auto_now=True)

    # Campos nuevos para recuperación de contraseña
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_expiration = models.DateTimeField(null=True, blank=True)

    def generar_token(self):
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expiration = timezone.now() + timedelta(hours=1)
        self.save()
        return self.reset_token

    def __str__(self):
        return self.usuario