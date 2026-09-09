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


class OfferRetrieveSerializer(serializers.ModelSerializer):
    details = OfferDetailListSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
            'details', 'min_price', 'min_delivery_time'
        ]

    def get_min_price(self, obj):
        result = obj.details.aggregate(Min("price"))
        return result['price__min']

    def get_min_delivery_time(self, obj):
        result = obj.details.aggregate(Min("delivery_time_in_days"))
        return result['delivery_time_in_days__min']


class OfferUpdateSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['title', 'details']

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)
        details = instance.details.all()
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type', None)
                detail = details.get(offer_type=offer_type)
                detail.title = detail_data.get('title', detail.title)
                detail.revisions = detail_data.get(
                    'revisions', detail.revisions)
                detail.delivery_time_in_days = detail_data.get(
                    'delivery_time_in_days', detail.delivery_time_in_days)
                detail.price = detail_data.get('price', detail.price)
                detail.features = detail_data.get('features', detail.features)
                detail.save()
        return instance

    def validate_details(self, value):
        for detail in value:
            if 'offer_type' not in detail:
                raise serializers.ValidationError("Each detail must include an offer_type.")
        return value