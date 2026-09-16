from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    """Represent a customer's review of a business user."""

    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='written_reviews')
    rating = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['reviewer', 'business_user'],
                name='unique_review_per_business_user'
            )
        ]

    def __str__(self):
        """Return the reviewed business user and rating."""
        return f'{self.business_user} ({self.rating}/5)'
