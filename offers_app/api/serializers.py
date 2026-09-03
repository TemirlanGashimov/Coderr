from django.contrib.auth.models import User
from rest_framework import serializers
from offers_app.models import OfferDetail, Offer
from django.db.models import Min


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'image', 'description', 'details'
        ]

    def validate(self, data):
        details = data.get('details')

        if len(details) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details."
            )

        offer_types = []

        for detail in details:
            offer_types.append(detail.get('offer_type'))

        if set(offer_types) != {'basic', 'standard', 'premium'}:
            raise serializers.ValidationError(
                "Details must contain basic, standard and premium"
            )

        return data

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)

        return offer


class OfferDetailListSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = [
            'id', 'url'
        ]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class OfferListSerializer(serializers.ModelSerializer):

    details = OfferDetailListSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time', 'user_details'
        ]

    def get_min_price(self, obj):
        result = obj.details.aggregate(Min("price"))
        return result['price__min']

    def get_min_delivery_time(self, obj):
        result = obj.details.aggregate(Min("delivery_time_in_days"))
        return result['delivery_time_in_days__min']
