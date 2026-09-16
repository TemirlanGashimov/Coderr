from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from orders_app.api.permissions import IsCustomer
from reviews_app.models import Review

from .permissions import IsReviewOwner
from .serializers import ReviewSerializer, ReviewUpdateSerializer


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    """List reviews or create one as an authenticated customer."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']
    pagination_class = None

    def perform_create(self, serializer):
        """Assign the authenticated user as the review author."""
        serializer.save(reviewer=self.request.user)

    def get_queryset(self):
        """Return reviews filtered by business user or reviewer."""
        queryset = Review.objects.all()
        business_user_id = self.request.query_params.get('business_user_id')
        if business_user_id is not None:
            queryset = queryset.filter(business_user_id=business_user_id)
        reviewer_id = self.request.query_params.get('reviewer_id')
        if reviewer_id is not None:
            queryset = queryset.filter(reviewer_id=reviewer_id)
        return queryset

    def get_permissions(self):
        """Require customer access for creation and authentication for reads."""
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsCustomer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a review owned by the requester."""
    queryset = Review.objects.all()
    serializer_class = ReviewUpdateSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]
