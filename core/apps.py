from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    #CHANGE: Ensure signals are registered when Django starts
    def ready(self):
        import core.signals
