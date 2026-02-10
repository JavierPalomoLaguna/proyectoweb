from django.test import TestCase, Client
from blog.models import Post, Categoria
from OnlyGlassWebApp.idioma import get_traducciones, TRADUCCIONES


class IdiomaTest(TestCase):
    """Tests para el sistema de idiomas"""
    
    def setUp(self):
        self.client = Client()
    
    def test_idioma_por_defecto_espanol(self):
        """Test que el idioma por defecto es español"""
        response = self.client.get('/')
        self.assertContains(response, 'Inicio')
    
    def test_cambio_a_ingles(self):
        """Test cambio de idioma a inglés"""
        response = self.client.get('/?lang=en')
        self.assertContains(response, 'Home')
    
    def test_persistencia_idioma(self):
        """Test que el idioma persiste en la sesión"""
        self.client.get('/?lang=en')
        response = self.client.get('/')
        self.assertContains(response, 'Home')
    
    def test_cambio_de_ingles_a_espanol(self):
        """Test cambio de inglés a español"""
        self.client.get('/?lang=en')
        response = self.client.get('/?lang=es')
        self.assertContains(response, 'Inicio')


class TraduccionesTest(TestCase):
    """Tests para el diccionario de traducciones"""
    
    def test_traducciones_espanol_existe(self):
        traducciones = get_traducciones('es')
        self.assertIn('inicio', traducciones)
        self.assertIn('contacto', traducciones)
        self.assertIn('categorias', traducciones)
    
    def test_traducciones_ingles_existe(self):
        traducciones = get_traducciones('en')
        self.assertIn('inicio', traducciones)
        self.assertIn('contacto', traducciones)
        self.assertIn('categorias', traducciones)
    
    def test_traducciones_valores_espanol(self):
        traducciones = get_traducciones('es')
        self.assertEqual(traducciones['inicio'], 'Inicio')
        self.assertEqual(traducciones['contacto'], 'Contacto')
    
    def test_traducciones_valores_ingles(self):
        traducciones = get_traducciones('en')
        self.assertEqual(traducciones['inicio'], 'Home')
        self.assertEqual(traducciones['contacto'], 'Contact')
    
    def test_idioma_invalido_devuelve_espanol(self):
        """Test que un idioma inválido devuelve español"""
        traducciones = get_traducciones('fr')
        self.assertEqual(traducciones['inicio'], 'Inicio')


class HomeViewTest(TestCase):
    """Tests para la vista home"""
    
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nombre="Test Categoria")
        self.post = Post.objects.create(
            titulo="Post Publicado",
            contenido_espanol="Contenido ES",
            contenido_ingles="Content EN",
            publicado=True
        )
        self.post.categorias.add(self.categoria)
        
        self.post_no_publicado = Post.objects.create(
            titulo="Post No Publicado",
            contenido_espanol="No visible",
            contenido_ingles="Not visible",
            publicado=False
        )
        self.post_no_publicado.categorias.add(self.categoria)
    
    def test_home_carga(self):
        """Test que home carga correctamente"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_home_muestra_posts_publicados(self):
        """Test que solo muestra posts publicados"""
        response = self.client.get('/')
        self.assertContains(response, "Post Publicado")
        self.assertNotContains(response, "Post No Publicado")
    
    def test_home_contenido_espanol(self):
        """Test contenido en español"""
        response = self.client.get('/?lang=es')
        self.assertContains(response, "Contenido ES")
    
    def test_home_contenido_ingles(self):
        """Test contenido en inglés"""
        response = self.client.get('/?lang=en')
        self.assertContains(response, "Content EN")
    
    def test_home_tiene_categorias(self):
        """Test que las categorías se muestran en el menú"""
        response = self.client.get('/')
        self.assertContains(response, "Test Categoria")


class PaginasLegalesTest(TestCase):
    """Tests para páginas legales"""
    
    def setUp(self):
        self.client = Client()
    
    def test_politica_privacidad(self):
        response = self.client.get('/politica-privacidad/')
        self.assertEqual(response.status_code, 200)
    
    def test_aviso_legal(self):
        response = self.client.get('/aviso-legal/')
        self.assertEqual(response.status_code, 200)
    
    def test_politica_cookies(self):
        response = self.client.get('/politica-cookies/')
        self.assertEqual(response.status_code, 200)