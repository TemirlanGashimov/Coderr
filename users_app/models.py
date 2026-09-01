from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):

    TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('busisness-user', 'Busisness User'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default='customer')

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.username} ({self.type})'
