from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import Permission, PermissionsMixin, User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Utilisateur(models.Model):
    ROLES_CHOICES = [
        ('admin', 'Administrateur'),
        ('manager', 'Manager'),
        ('utilisateur', 'Utilisateur'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE) # Relation entre la class Utilisateur et User
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, default='utilisateur') # La valeur par defaut de role

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    # Enregistrement automatique du role une fois que l'utilisateur est créé
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Utilisateur.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.utilisateur.save()
