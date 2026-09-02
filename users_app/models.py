from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):

    TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, default='customer')
    file = models.FileField(upload_to='user_files/', default="", blank=True)
    location = models.CharField(max_length=255, default="", blank=True)
    tel = models.CharField(max_length=20, default="", blank=True)
    description = models.TextField(default="", blank=True)
    working_hours = models.CharField(max_length=100, default="", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.user} ({self.type})'
