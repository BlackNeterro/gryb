from django.apps import AppConfig
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name'

    def ready(self):
        import gryb_app.signals  # Import the signals.py file here

