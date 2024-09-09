from django.contrib.auth.models import User
from django.db import models

# Table Profile (pour informations utilisateur supplémentaires)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Correct ForeignKey
    biographie = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username
