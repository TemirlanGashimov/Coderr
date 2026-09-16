from django.db.models import Avg

from rest_framework import generics
from rest_framework.response import Response

from offers_app.models import Offer
from reviews_app.models import Review
from users_app.models import UserProfile


class BaseInfoAPIView(generics.GenericAPIView):
    """Return aggregate statistics used by the dashboard."""

    def get(self, request, format=None):
        """Return counts and the average review rating."""
        review_count = Review.objects.all().count()
        average_rating = Review.objects.all().aggregate(
            average_rating=Avg('rating', default=0))
        average_rating = round(average_rating['average_rating'], 1)
        business_profile_count = UserProfile.objects.all().filter(type='business').count()
        offer_count = Offer.objects.all().count()
        return Response(data={"review_count": review_count, "average_rating": average_rating,
                              "business_profile_count": business_profile_count, "offer_count": offer_count})
