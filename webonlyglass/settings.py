import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

ENV = config('DJANGO_ENV', default='local')

SITE_ID = 1

if ENV == 'production':
    DEBUG = False
    ALLOWED_HOSTS = ['onlyglass.es', 'www.onlyglass.es']
    CSRF_TRUSTED_ORIGINS = ['https://onlyglass.es', 'https://www.onlyglass.es']
    
    # Configuración automática del Site para producción
    try:
        from django.contrib.sites.models import Site
        site = Site.objects.get(id=1)
        site.domain = 'onlyglass.es'
        site.name = 'Only Glass'
        site.save()
    except:
        pass  # Se creará con el comando de setup
    
else:
    DEBUG = True
    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '.ngrok-free.dev',
        '.localhost',
        '0.0.0.0',
        'testserver',
    ]
    CSRF_TRUSTED_ORIGINS = [
        'https://*.ngrok-free.dev',
        'http://localhost:8000',
        'http://127.0.0.1:8000',
    ]
    
    # Configuración automática del Site para desarrollo
    try:
        from django.contrib.sites.models import Site
        site = Site.objects.get(id=1)
        site.domain = 'localhost:8000'
        site.name = 'Only Glass - Desarrollo'
        site.save()
    except:
        pass  # Se creará con el comando de setup

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',      
    'django.contrib.sitemaps',   
    'OnlyGlassWebApp',
    'blog',
    'contacto',
    'crispy_forms',
    'crispy_bootstrap4',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',    
    ]

ROOT_URLCONF = 'webonlyglass.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'webonlyglass', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages', 
                'OnlyGlassWebApp.context_processors.datos_globales',                
            ],
        },
    },
]

WSGI_APPLICATION = 'webonlyglass.wsgi.application'

# Configuración de base de datos según entorno
if ENV == 'production':
    # PostgreSQL para producción
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
else:
    # SQLite para desarrollo local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-eu'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'OnlyGlassWebApp/static'),
]

# Archivos multimedia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
#EMAIL_HOST_USER = 'jpalomolaguna@gmail.com'
EMAIL_HOST_USER = 'onlyglasscurtains@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

SESSION_COOKIE_AGE = 1209600  # 2 semanas
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

