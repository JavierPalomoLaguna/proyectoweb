from django.db import models
from tienda.models import Productos
from clientes.models import Cliente

# Create your models here.

class ConfiguracionEnvio(models.Model):
    umbral_envio_gratis = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=300.00,
        verbose_name="Umbral para envío gratis (€)"
    )
    costo_envio_estandar = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=5.95,
        verbose_name="Costo envío estándar (€)"
    )
    activo = models.BooleanField(default=True, verbose_name="Configuración activa")
    
    class Meta:
        verbose_name = 'configuración de envío'
        verbose_name_plural = 'configuraciones de envío'
    
    def __str__(self):
        return f"Envío: {self.costo_envio_estandar}€ / Gratis desde {self.umbral_envio_gratis}€"
    
    def save(self, *args, **kwargs):
        # Solo permitir una configuración activa
        if self.activo:
            ConfiguracionEnvio.objects.exclude(pk=self.pk).update(activo=False)
        super().save(*args, **kwargs)

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False)
    metodo_pago = models.CharField(max_length=20, choices=[('tarjeta', 'Tarjeta'), ('bizum', 'Bizum')])
    enviado = models.BooleanField(default=False, verbose_name="Pedido enviado")
    fecha_envio = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de envío")
    gastos_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Gastos de envío")
    envio_gratis = models.BooleanField(default=False, verbose_name="Envío gratis")

    # Campos adicionales para trazabilidad Redsys
    codigo_autorizacion = models.CharField(max_length=10, blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    hora_pago = models.TimeField(blank=True, null=True)
    pais_tarjeta = models.CharField(max_length=5, blank=True, null=True)
    identificador_comercio = models.CharField(max_length=20, blank=True, null=True)
    
    # ✅ NUEVO: CAMPOS PARA TRACKING DE ERRORES
    codigo_respuesta = models.CharField(max_length=10, blank=True, null=True, verbose_name="Código Respuesta Redsys")
    descripcion_error = models.CharField(max_length=100, blank=True, null=True, verbose_name="Descripción Error")
    fecha_intento = models.DateTimeField(blank=True, null=True, verbose_name="Fecha Intento Pago")

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre}"

    # ✅ AGREGAR ESTA PROPERTY QUE FALTA
    @property
    def total(self):
        return sum(linea.subtotal for linea in self.lineapedido_set.all())
    
    
class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'línea de pedido'
        verbose_name_plural = 'líneas de pedido'

    @property
    def subtotal(self):
        return self.producto.precio_total * self.cantidad
