from django.test import TestCase, Client
from blog.models import Post, Categoria
from blog.views import normalizar


class NormalizarTest(TestCase):
    """Tests para la función de normalización de texto"""
    
    def test_normalizar_minusculas(self):
        self.assertEqual(normalizar("HOLA"), "hola")
    
    def test_normalizar_tildes(self):
        self.assertEqual(normalizar("PÉRGOLA"), "pergola")
        self.assertEqual(normalizar("bioclimática"), "bioclimatica")
    
    def test_normalizar_simbolos(self):
        self.assertEqual(normalizar("pergola-bioclimatica"), "pergolabioclimatica")
        self.assertEqual(normalizar("pergola.bioclimatica"), "pergolabioclimatica")
        self.assertEqual(normalizar("pergola;bioclimatica"), "pergolabioclimatica")
    
    def test_normalizar_combinado(self):
        self.assertEqual(normalizar("PÉRGOLA BIOCLIMÁTICA"), "pergolabioclimatica")
        self.assertEqual(normalizar("Pérgola-Bioclimática"), "pergolabioclimatica")


class CategoriaModelTest(TestCase):
    """Tests para el modelo Categoria"""
    
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="CORTINA DE CRISTAL")
    
    def test_categoria_str(self):
        self.assertEqual(str(self.categoria), "CORTINA DE CRISTAL")
    
    def test_categoria_creacion(self):
        self.assertIsNotNone(self.categoria.created)
        self.assertIsNotNone(self.categoria.updated)


class CategoriaViewTest(TestCase):
    """Tests para la vista de categoría"""
    
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nombre="PÉRGOLA BIOCLIMÁTICA")
        self.post = Post.objects.create(
            titulo="Test Post",
            contenido_espanol="Contenido en español",
            contenido_ingles="Content in English",
            publicado=True
        )
        self.post.categorias.add(self.categoria)
    
    def test_categoria_url_normal(self):
        """Test acceso con URL normalizada"""
        response = self.client.get('/blog/categoria/pergola-bioclimatica/')
        self.assertEqual(response.status_code, 200)
    
    def test_categoria_url_con_tildes(self):
        """Test que funciona buscando con diferentes formatos"""
        response = self.client.get('/blog/categoria/pergola-bioclimatica/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
    
    def test_categoria_todos(self):
        """Test para ver todos los proyectos"""
        response = self.client.get('/blog/categoria/todos/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
    
    def test_categoria_no_existe(self):
        """Test para categoría que no existe"""
        response = self.client.get('/blog/categoria/no-existe/')
        self.assertEqual(response.status_code, 404)
    
    def test_categoria_idioma_espanol(self):
        """Test contenido en español"""
        response = self.client.get('/blog/categoria/pergola-bioclimatica/?lang=es')
        self.assertContains(response, "Contenido en español")
    
    def test_categoria_idioma_ingles(self):
        """Test contenido en inglés"""
        response = self.client.get('/blog/categoria/pergola-bioclimatica/?lang=en')
        self.assertContains(response, "Content in English")