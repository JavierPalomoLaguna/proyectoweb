from django.conf import settings
from ventas.models import ConfiguracionEnvio

def importe_total_carro(request):
    total = 0
    if "carro" in request.session:
        for key, value in request.session["carro"].items():
            total += float(value["precio"]) * value["cantidad"]
    return {"importe_total_carro": total}

def productos_total_carro(request):
    total = 0
    if "carro" in request.session:
        for key, value in request.session["carro"].items():
            total += int(value["cantidad"])
    return {"productos_total_carro": total}

def gastos_envio_carro(request):
    total = 0
    if "carro" in request.session:
        for key, value in request.session["carro"].items():
            total += float(value["precio"]) * value["cantidad"]
    
    # ✅ DEBUG: VER QUÉ ESTÁ PASANDO
    try:
        config_envio = ConfiguracionEnvio.objects.get(activo=True)
        umbral = float(config_envio.umbral_envio_gratis)
        costo_envio = float(config_envio.costo_envio_estandar)
    except ConfiguracionEnvio.DoesNotExist as e:
        print(f"❌ DEBUG: No se encontró configuración activa: {e}")
        umbral = getattr(settings, 'UMBRAL_ENVIO_GRATIS', 300.00)
        costo_envio = getattr(settings, 'GASTOS_ENVIO', 5.95)
    
    
    
    if total >= umbral:
        gastos_envio = 0
    else:
        gastos_envio = costo_envio
    
    return {"gastos_envio_carro": gastos_envio}

def total_con_envio_carro(request):
    total = 0
    if "carro" in request.session:
        for key, value in request.session["carro"].items():
            total += float(value["precio"]) * value["cantidad"]
    
    try:
        config_envio = ConfiguracionEnvio.objects.get(activo=True)
        umbral = float(config_envio.umbral_envio_gratis)
        costo_envio = float(config_envio.costo_envio_estandar)
    except ConfiguracionEnvio.DoesNotExist:
        umbral = getattr(settings, 'UMBRAL_ENVIO_GRATIS', 300.00)
        costo_envio = getattr(settings, 'GASTOS_ENVIO', 5.95)
    
    if total >= umbral:
        total_con_envio = total
    else:
        total_con_envio = total + costo_envio
    
    return {"total_con_envio_carro": total_con_envio}

def envio_gratis_info(request):
    total = 0
    if "carro" in request.session:
        for key, value in request.session["carro"].items():
            total += float(value["precio"]) * value["cantidad"]
    
    # ✅ OBTENER CONFIGURACIÓN DE LA BBDD
    try:
        config_envio = ConfiguracionEnvio.objects.get(activo=True)
        # ✅ CONVERTIR Decimal A float
        umbral = float(config_envio.umbral_envio_gratis)
    except ConfiguracionEnvio.DoesNotExist:
        umbral = getattr(settings, 'UMBRAL_ENVIO_GRATIS', 300.00)
    
    # Información sobre envío gratis
    envio_gratis = total >= umbral
    falta_para_envio_gratis = max(0, umbral - total)
    
    return {
        "envio_gratis_carro": envio_gratis,
        "falta_para_envio_gratis": falta_para_envio_gratis,
        "umbral_envio_gratis": umbral,
    }