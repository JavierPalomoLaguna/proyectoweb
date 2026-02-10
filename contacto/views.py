from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import FormularioContacto
from .models import MensajeContacto
from django.conf import settings
from urllib.parse import quote
from django.urls import reverse
from OnlyGlassWebApp.idioma import get_idioma
from blog.models import Categoria


def contacto(request):
    lang = get_idioma(request)
    
    # Si viene con parámetro de éxito (después de redirigir)
    mensaje_exito = request.GET.get('mensaje_exito', None)
    
    if request.method == "POST":
        formulario = FormularioContacto(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data["name"]
            email = formulario.cleaned_data["email"]
            contenido = formulario.cleaned_data["contenido"]

            # Guardar en BD
            MensajeContacto.objects.create(
                nombre=nombre,
                email=email,
                contenido=contenido
            )

            # Enviar correo
            send_mail(
                subject="Nuevo mensaje de contacto - Only Glass",
                message=f"Nombre: {nombre}\nEmail: {email}\nContenido:\n{contenido}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['onlyglasscurtains@gmail.com'], 
                fail_silently=False,
            )
            
            # DETECTAR si viene de home.html
            if request.POST.get('from_home') == 'true':
                mensaje_exito_texto = "¡Mensaje enviado correctamente! Te contactaremos pronto."
                mensaje_codificado = quote(mensaje_exito_texto.encode('utf-8').decode('utf-8'))
                return redirect(f'/?mensaje={mensaje_codificado}')
            
            # Redirigir a contacto con mensaje de éxito
            mensaje_codificado = quote("¡Mensaje enviado correctamente! Te contactaremos pronto.")
            return redirect(f'{reverse("contacto")}?mensaje_exito={mensaje_codificado}')
    
    # GET request: siempre formulario vacío
    formulario = FormularioContacto()
    
    # Obtener categorías para el menú
    categorias_unicas = Categoria.objects.all()
    
    return render(request, "contacto/contacto.html", {
        "formulario": formulario,
        "mensaje_exito": mensaje_exito,
        "idioma_actual": lang,
        "categorias_unicas": categorias_unicas,
    })