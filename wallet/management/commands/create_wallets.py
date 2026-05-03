from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wallet.models import Wallet

User = get_user_model()

class Command(BaseCommand):
    help = 'Create wallets for users who do not have one'

    def handle(self, *args, **options):
        users_without_wallet = User.objects.filter(wallet__isnull=True)
        for user in users_without_wallet:
            Wallet.objects.create(user=user)
            self.stdout.write(f'Created wallet for user: {user.username}')
        self.stdout.write(f'Created wallets for {users_without_wallet.count()} users')