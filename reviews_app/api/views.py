from rest_framework import generics
from reviews_app.models import Review
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from orders_app.api.permissions import IsCustomer
from rest_framework import filters


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def get_queryset(self):
        queryset = Review.objects.all()
        business_user_id = self.request.query_params.get('business_user_id')
        if business_user_id is not None:
            queryset = queryset.filter(business_user_id=business_user_id)
        reviewer_id = self.request.query_params.get('reviewer_id')
        if reviewer_id is not None:
            queryset = queryset.filter(reviewer_id=reviewer_id)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsCustomer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]