from rest_framework import generics
from reviews_app.models import Reviews
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from orders_app.api.permissions import IsCustomer


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        serializer.save(reviewer = self.request.user)