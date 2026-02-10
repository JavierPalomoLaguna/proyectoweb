TRADUCCIONES = {
    'es': {
        # Menú
        'inicio': 'Inicio',
        'categorias': 'Categorías',
        'contacto': 'Contacto',
        'no_hay_categorias': 'No hay categorías',
        
        # Hero
        'hero_titulo': 'Only Glass',
        'hero_subtitulo': 'Especialistas en carpintería y acristalamiento',
        'hero_descripcion': 'En Only Glass transformamos terrazas, porches y exteriores en lugares únicos, confortables y llenos de luz. Con más de 15 años de experiencia en el sector, ofrecemos soluciones de alta calidad con un enfoque moderno, eficiente y totalmente personalizado. Disfruta de tu terraza, porche, jardín o balcón los 365 días del año con nuestros sistemas de cerramientos de cristal sin perfiles de aluminio y las pérgolas bioclimáticas.',
        
        # Home
        'nuestros_proyectos': 'Nuestros Proyectos',
        'ver_mas': 'Ver más',
        'ver_todos_proyectos': 'Ver todos los proyectos',
        'no_hay_proyectos': 'No hay proyectos disponibles.',
        'donde_estamos': 'Dónde estamos',
        'info_contacto': 'Información de contacto',
        'direccion': 'Dirección',
        'telefono': 'Teléfono',
        'email': 'Email',
        'horario': 'Horario',
        'horario_valor': 'L-V 9:00-14:00 / 17:00-20:00',
        
        # Formulario
        'nombre': 'Nombre',
        'mensaje': 'Mensaje',
        'enviar_mensaje': 'Enviar mensaje',
        'pagina_contacto': '¿Prefieres la página completa de contacto?',
        'ir_contacto': 'Ir a página de contacto',
        
        # Footer
        'politica_privacidad': 'Política de privacidad',
        'aviso_legal': 'Aviso legal',
        'cookies': 'Cookies',
        'derechos': 'Todos los derechos reservados.',
    },
    'en': {
        # Menú
        'inicio': 'Home',
        'categorias': 'Categories',
        'contacto': 'Contact',
        'no_hay_categorias': 'No categories',
        
        # Hero
        'hero_titulo': 'Only Glass',
        'hero_subtitulo': 'Specialists in carpentry and glazing',
        'hero_descripcion': 'At Only Glass we transform terraces, porches and exteriors into unique, comfortable and bright spaces. With over 15 years of experience in the sector, we offer high-quality solutions with a modern, efficient and fully personalized approach. Enjoy your terrace, porch, garden or balcony 365 days a year with our frameless glass enclosure systems and bioclimatic pergolas.',
        
        # Home
        'nuestros_proyectos': 'Our Projects',
        'ver_mas': 'See more',
        'ver_todos_proyectos': 'See all projects',
        'no_hay_proyectos': 'No projects available.',
        'donde_estamos': 'Where we are',
        'info_contacto': 'Contact information',
        'direccion': 'Address',
        'telefono': 'Phone',
        'email': 'Email',
        'horario': 'Hours',
        'horario_valor': 'Mon-Fri 9:00-14:00 / 17:00-20:00',
        
        # Formulario
        'nombre': 'Name',
        'mensaje': 'Message',
        'enviar_mensaje': 'Send message',
        'pagina_contacto': 'Prefer the full contact page?',
        'ir_contacto': 'Go to contact page',
        
        # Footer
        'politica_privacidad': 'Privacy policy',
        'aviso_legal': 'Legal notice',
        'cookies': 'Cookies',
        'derechos': 'All rights reserved.',
    }
}


def get_idioma(request):
    """Obtiene el idioma de la URL o de la sesión"""
    lang = request.GET.get('lang', None)
    
    if lang:
        request.session['idioma'] = lang
    else:
        lang = request.session.get('idioma', 'es')
    
    return lang


def get_traducciones(lang):
    """Devuelve el diccionario de traducciones para el idioma"""
    return TRADUCCIONES.get(lang, TRADUCCIONES['es'])