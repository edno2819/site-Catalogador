from django.apps import AppConfig


class BuscasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'buscas'

    def ready(self):...
        # from buscas import screduler
        # screduler.extracts()