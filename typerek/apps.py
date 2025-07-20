from django.apps import AppConfig


class TyperekConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'typerek'

    def ready(self):
        import typerek.signals
