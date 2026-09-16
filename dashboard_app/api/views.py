from rest_framework import generics
from reviews_app.models import Review
from django.db.models import Avg
from users_app.models import UserProfile
from offers_app.models import Offer
from rest_framework.response import Response


class BaseInfoAPIView(generics.GenericAPIView):
    def get(self, request, format=None):
        review_count = Review.objects.all().count()
        average_rating = Review.objects.all().aggregate(average_rating=Avg('rating', default=0))
        average_rating = round(average_rating['average_rating'], 1)
        business_profile_count = UserProfile.objects.all().filter(type='business').count()
        offer_count = Offer.objects.all().count()
        return Response(data={"review_count": review_count, "average_rating": average_rating,
                 "business_profile_count": business_profile_count, "offer_count": offer_count})
