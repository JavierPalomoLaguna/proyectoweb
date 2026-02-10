from django.urls import path
from OnlyGlassWebApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='base'),
    path('home/', views.home, name='home'),
    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('aviso-legal/', views.aviso_legal, name='aviso_legal'),
]

# Esto solo en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)