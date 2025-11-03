from django.shortcuts import render
from django.core.mail import send_mail
from .forms import FormularioContacto
from .models import MensajeContacto
from django.conf import settings

def contacto(request):
    mensaje_exito = None

    if request.method == "POST":
        formulario = FormularioContacto(request.POST)
        if formulario.is_valid():
            nombre = formulario.cleaned_data["name"]
            email = formulario.cleaned_data["email"]
            contenido = formulario.cleaned_data["contenido"]

            # Guardar en la base de datos
            MensajeContacto.objects.create(
                nombre=nombre,
                email=email,
                contenido=contenido
            )

            # Enviar correo
            send_mail(
                subject="Nuevo mensaje de contacto",
                message=f"Nombre: {nombre}\nEmail: {email}\nContenido:\n{contenido}",
                from_email=settings.EMAIL_HOST_USER,  # ← debe ser 'jpalomolaguna@gmail.com'
                recipient_list=['jpalomolaguna@gmail.com'],  # ← puede ser otro correo
                fail_silently=False,
            )

            mensaje_exito = "Mensaje enviado correctamente."
            formulario = FormularioContacto()
    else:
        formulario = FormularioContacto()

    return render(request, "contacto/contacto.html", {
        "formulario": formulario,
        "mensaje_exito": mensaje_exito
    })
