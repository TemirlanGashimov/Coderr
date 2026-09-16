from django.shortcuts import get_object_or_404

from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serialize orders and create them from an offer detail."""

    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            'offer_detail_id', 'id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price',
            'features', 'offer_type', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price',
                            'features', 'offer_type', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Create an order using a snapshot of the selected offer detail."""
        offer_detail_id = validated_data.pop('offer_detail_id')
        offer_detail = get_object_or_404(OfferDetail, pk=offer_detail_id)
        customer_user = self.context['request'].user

        order = Order.objects.create(title=offer_detail.title, revisions=offer_detail.revisions,
                                     delivery_time_in_days=offer_detail.delivery_time_in_days, price=offer_detail.price, features=offer_detail.features,
                                     offer_type=offer_detail.offer_type, business_user=offer_detail.offer.user, customer_user=customer_user)

        return order


class OrderStatusSerializer(serializers.ModelSerializer):
    """Serialize the mutable status field of an order."""
    class Meta:
        model = Order
        fields = ['status']
