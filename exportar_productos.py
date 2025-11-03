from django.core.management import call_command

with open('fixtures/productos.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 'tienda.Productos', indent=2, stdout=f)
