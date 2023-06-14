from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        email = input('Email: ')
        password = input('Password: ')

        # Создание суперпользователя
        User.objects.create_superuser(email=email, password=password)

        self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
