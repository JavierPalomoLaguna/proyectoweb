from .models import Cliente

def cliente_context(request):
    cliente = None
    cliente_id = request.session.get('cliente_id')
    if cliente_id:
        try:
            cliente = Cliente.objects.get(id=cliente_id)
        except Cliente.DoesNotExist:
            pass
    return {'cliente': cliente}