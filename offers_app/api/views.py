from rest_framework import filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from offers_app.models import Offer, OfferDetail

from .permissions import IsBusinessUser, IsCreatorOffers
from .filters import OfferFilterBackend
from .serializers import OfferSerializer, OfferListSerializer, OfferRetrieveSerializer, OfferUpdateSerializer, OfferDetailSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """Provide bounded pagination for offer list responses."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferListCreateAPIView(generics.ListCreateAPIView):
    """List offers or create an offer for a business user."""
    queryset = Offer.objects.all()
    permission_classes = [IsBusinessUser]
    pagination_class = StandardResultsSetPagination
    serializer_class = OfferSerializer
    filter_backends = [OfferFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['-updated_at']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        """Use a compact serializer for lists and a nested one for creates."""
        if self.request.method == 'GET':
            return OfferListSerializer
        return OfferSerializer

    def create(self, request, *args, **kwargs):
        """Validate and persist a new offer."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """Assign the authenticated user as the offer owner."""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """Return the base offer queryset for filter backends."""
        return Offer.objects.all()


class OfferRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an offer owned by the requester."""
    queryset = Offer.objects.all()
    serializer_class = OfferRetrieveSerializer
    permission_classes = [IsAuthenticated, IsCreatorOffers]

    def get_serializer_class(self):
        """Use the update serializer only for partial updates."""
        if self.request.method == 'PATCH':
            return OfferUpdateSerializer
        return OfferRetrieveSerializer

    def partial_update(self, request, *args, **kwargs):
        """Update an offer and return its complete nested representation."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = OfferSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class OfferDetailRetrieveAPIView(generics.RetrieveAPIView):
    """Return one offer detail for authenticated clients."""
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
