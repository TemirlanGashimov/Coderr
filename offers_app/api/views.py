from offers_app.models import Offer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .permissions import IsBusinessUser
from django.db.models import Min


from .serializers import OfferSerializer, OfferListSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class OfferListCreateAPIView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    permission_classes = [IsBusinessUser]
    pagination_class = StandardResultsSetPagination
    serializer_class = OfferSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferListSerializer
        return OfferSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def get_queryset(self):
        queryset = Offer.objects.all()

        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            queryset = queryset.filter(user__id=creator_id)

        queryset = queryset.annotate(min_price=Min('details__price'))
        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)

        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            queryset = queryset.annotate(min_delivery_time=Min('details__delivery_time_in_days'))
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time)

        return queryset 

