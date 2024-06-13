from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Customer

class Command(BaseCommand):
    help = 'Create Customer objects for users without them'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            if not hasattr(user, 'customer'):
                Customer.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Created customer for user {user.username}'))
