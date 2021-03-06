from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+2_6c0*5fe^_bqjs5i)546-ei)5*(vqyce(8qiay6$se!h!-%+'


DEBUG = True
ALLOWED_HOSTS = []
#ALLOWED_HOSTS = ['rox-catalogador.herokuapp.com', '127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'buscas.apps.BuscasConfig' 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'catalogador.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'catalogador.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#cron jobs :https://gutsytechster.wordpress.com/2019/06/24/how-to-setup-a-cron-job-in-django/
# Minuto (0 - 59)
# Hora (0 - 23)
# Dia do m??s (1 ??? 31)
# M??s (1 - 12)
# Dia da semana (0 - 6)
#TAREFAZ EXECUTADAS DE FORMA PARALELAS
# CRON_LOG = '>> /home/edno/Desktop/Catalogador/site-Catalogador/catalogador/logs/cron_log.log'
# CRONJOBS = [
#     #('4 16 * * 2,3,4,5,6', 'buscas.cron.deleteVelasBefore', CRON_LOG),
#     # ('* 13 * * 1,2,3,4,5', 'buscas.cron.extract_1_1_Django', CRON_LOG),
#     # ('1 0 * * 2,3,4,5,6', 'buscas.cron.extract_1_2_Django', CRON_LOG),
#     # ('6 0 * * 2,3,4,5,6', 'buscas.cron.extract_5_Django', CRON_LOG),
#     # ('8 0 * * 2,3,4,5,6', 'buscas.cron.extract_15_Django', CRON_LOG),
#     #('* * * * *', 'buscas.cron.ResetValues', CRON_LOG),
# ]

#redireciona os erros para stdoutc
# CRONTAB_COMMAND_SUFFIX = '2>&1'
# python3 manage.py crontab add
# python3 manage.py crontab show
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240