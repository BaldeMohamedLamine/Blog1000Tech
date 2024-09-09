from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Account.models import Profile

class Command(BaseCommand):
    help = 'Crée des profils pour tous les utilisateurs qui n\'en ont pas'

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            Profile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Profil créé pour l\'utilisateur {user.username}'))
