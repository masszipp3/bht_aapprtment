from django.apps import AppConfig


class BhtaptWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bhtapt_web'

    def ready(self):
        # Importing the signals here ensures they are registered when Django starts
        import bhtapt_web.signals
