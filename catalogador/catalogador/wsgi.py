import os
from django.core.wsgi import get_wsgi_application        
from buscas import screduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogador.settings')
application = get_wsgi_application()
screduler.extracts()
