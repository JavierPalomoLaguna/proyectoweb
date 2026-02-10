from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Categoria
from django.utils.text import slugify


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['home', 'contacto']

    def location(self, item):
        return reverse(item)


class CategoriaSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return Categoria.objects.all()

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return f'/blog/categoria/{slugify(obj.nombre)}/'