from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    """Represent an offer published by a business user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offer_images/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the offer title."""
        return self.title


class OfferDetail(models.Model):
    """Represent one pricing tier belonging to an offer."""
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey(
        Offer, on_delete=models.CASCADE, related_name='details')

    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=30, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        """Return the tier title and type."""
        return f'{self.title} ({self.offer_type})'
