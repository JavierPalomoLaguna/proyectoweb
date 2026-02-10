from django.test import TestCase, Client
from django.urls import reverse
from contacto.models import MensajeContacto
from contacto.forms import FormularioContacto


class FormularioContactoTest(TestCase):
    """Tests para el formulario de contacto"""
    
    def test_formulario_valido(self):
        form_data = {
            'name': 'Juan',
            'email': 'juan@example.com',
            'contenido': 'Este es un mensaje de prueba'
        }
        form = FormularioContacto(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_formulario_sin_nombre(self):
        form_data = {
            'name': '',
            'email': 'juan@example.com',
            'contenido': 'Mensaje'
        }
        form = FormularioContacto(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_formulario_email_invalido(self):
        form_data = {
            'name': 'Juan',
            'email': 'email-invalido',
            'contenido': 'Mensaje'
        }
        form = FormularioContacto(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_formulario_sin_mensaje(self):
        form_data = {
            'name': 'Juan',
            'email': 'juan@example.com',
            'contenido': ''
        }
        form = FormularioContacto(data=form_data)
        self.assertFalse(form.is_valid())


class ContactoViewTest(TestCase):
    """Tests para la vista de contacto"""
    
    def setUp(self):
        self.client = Client()
    
    def test_contacto_get(self):
        """Test que la página de contacto carga correctamente"""
        response = self.client.get(reverse('contacto'))
        self.assertEqual(response.status_code, 200)
    
    def test_contacto_idioma_espanol(self):
        """Test página de contacto en español"""
        response = self.client.get(reverse('contacto') + '?lang=es')
        self.assertEqual(response.status_code, 200)
    
    def test_contacto_idioma_ingles(self):
        """Test página de contacto en inglés"""
        response = self.client.get(reverse('contacto') + '?lang=en')
        self.assertEqual(response.status_code, 200)


class MensajeContactoModelTest(TestCase):
    """Tests para el modelo MensajeContacto"""
    
    def test_crear_mensaje(self):
        mensaje = MensajeContacto.objects.create(
            nombre='Juan',
            email='juan@example.com',
            contenido='Mensaje de prueba'
        )
        self.assertEqual(mensaje.nombre, 'Juan')
        self.assertEqual(mensaje.email, 'juan@example.com')
        self.assertIsNotNone(mensaje.id)