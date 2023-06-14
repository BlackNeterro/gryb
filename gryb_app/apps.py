from django.apps import AppConfig


class GrybAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gryb_app'

from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gryb_app'  # Замените на имя вашего приложения
    verbose_name = 'gryb_app'  # Замените на название вашего приложения
    def ready(self):
        import gryb_app.signals  # Замените на имя вашего приложения

class GrybAppConfig(AppConfig):
    name = 'gryb_app'

    def ready(self):
        import gryb_app.signals
