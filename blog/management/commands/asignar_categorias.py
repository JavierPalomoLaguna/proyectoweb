import json
from django.core.management.base import BaseCommand
from blog.models import Post, Categoria

class Command(BaseCommand):
    help = 'Asigna categorías a posts desde un JSON con estructura tipo fixture'

    def handle(self, *args, **kwargs):
        try:
            with open('relaciones_post_categoria.json', encoding='utf-8') as f:
                relaciones = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✘ Error al leer el archivo: {e}"))
            return

        for r in relaciones:
            try:
                campos = r["fields"]
                post = Post.objects.get(pk=campos["post"])
                categoria = Categoria.objects.get(pk=campos["categoria"])
                post.categorias.add(categoria)
                self.stdout.write(self.style.SUCCESS(
                    f"✔ Asignada categoría '{categoria.nombre}' al post '{post.titulo}'"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"✘ Error con post_id={r.get('fields', {}).get('post')} y categoria_id={r.get('fields', {}).get('categoria')}: {e}"
                ))
