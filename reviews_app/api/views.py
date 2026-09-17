from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders_app.api.permissions import IsCustomer
from reviews_app.models import Review

from .permissions import IsReviewOwner
from .filters import ReviewFilterBackend
from .serializers import ReviewSerializer, ReviewUpdateSerializer


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    """List reviews or create one as an authenticated customer."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [ReviewFilterBackend, filters.OrderingFilter]
    ordering_fields = ['updated_at', 'rating']
    pagination_class = None

    def perform_create(self, serializer):
        """Assign the authenticated user as the review author."""
        serializer.save(reviewer=self.request.user)

    def get_queryset(self):
        """Return the base review queryset for filter backends."""
        return Review.objects.all()

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

    def update(self, request, *args, **kwargs):
        """Update a review and return its complete representation."""
        instance = self.get_object()
        serializer = ReviewUpdateSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = ReviewSerializer(instance)
        return Response(response_serializer.data)
