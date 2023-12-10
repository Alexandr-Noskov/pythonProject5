from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Добавляем админа"""
        user = User.objects.create(
            email='san9nosko8@gmail.com',
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password('1408')
        user.save()