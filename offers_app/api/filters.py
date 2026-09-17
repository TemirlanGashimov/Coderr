from django.db.models import Min
from rest_framework.filters import BaseFilterBackend


class OfferFilterBackend(BaseFilterBackend):
    """Filter offers by creator, minimum price, and delivery time."""

    def filter_queryset(self, request, queryset, view):
        queryset = queryset.annotate(min_price=Min('details__price'))
        queryset = self._filter_creator(request, queryset)
        queryset = self._filter_price(request, queryset)
        return self._filter_delivery_time(request, queryset)

    def _filter_creator(self, request, queryset):
        creator_id = request.query_params.get('creator_id')
        return queryset.filter(user__id=creator_id) if creator_id else queryset

    def _filter_price(self, request, queryset):
        min_price = request.query_params.get('min_price')
        return queryset.filter(min_price__gte=min_price) if min_price else queryset

    def _filter_delivery_time(self, request, queryset):
        max_delivery_time = request.query_params.get('max_delivery_time')
        if not max_delivery_time:
            return queryset
        queryset = queryset.annotate(
            min_delivery_time=Min('details__delivery_time_in_days'))
        return queryset.filter(min_delivery_time__lte=max_delivery_time)