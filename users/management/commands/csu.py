from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(phone='89123456789',
                                   first_name='Admin',
                                   last_name='Adminov',
                                   is_superuser=True,
                                   is_staff=True,
                                   is_active=True)
        user.set_password('123qw456er')
        user.save()
