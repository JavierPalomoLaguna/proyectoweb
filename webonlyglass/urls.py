from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from OnlyGlassWebApp.sitemaps import StaticViewSitemap, CategoriaSitemap
from django.views.generic import RedirectView  
from django.conf import settings  
from django.conf.urls.static import static 
from OnlyGlassWebApp import views 


sitemaps = {
    'static': StaticViewSitemap,
    'categorias': CategoriaSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('OnlyGlassWebApp.urls')),
    path('blog/', include('blog.urls')),
    path('contacto/', include('contacto.urls')),  
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', RedirectView.as_view(url='/static/OnlyGlassWebApp/robots.txt', permanent=True)),
    path('politica-cookies/', views.politica_cookies, name='politica_cookies'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)