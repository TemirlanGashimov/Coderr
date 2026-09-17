from django.contrib.auth.models import User
from django.db.models import Min
from rest_framework import serializers
from offers_app.models import OfferDetail, Offer



class OfferDetailSerializer(serializers.ModelSerializer):
    """Serialize the fields of one offer pricing tier."""
    class Meta:
        model = OfferDetail
        fields = [
            'id', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type'
        ]


class OfferSerializer(serializers.ModelSerializer):
    """Serialize offers and create their three pricing tiers."""
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'image', 'description', 'details'
        ]

    def validate(self, data):
        """Require exactly one basic, standard, and premium tier."""
        details = data.get('details')
        self._validate_detail_count(details)
        self._validate_detail_types(details)
        return data

    def _validate_detail_count(self, details):
        if len(details) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 details.")

    def _validate_detail_types(self, details):
        offer_types = {detail.get('offer_type') for detail in details}
        if offer_types != {'basic', 'standard', 'premium'}:
            raise serializers.ValidationError(
                "Details must contain basic, standard and premium")

    def create(self, validated_data):
        """Create an offer together with its nested pricing tiers."""
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        self._create_details(offer, details_data)
        return offer

    def _create_details(self, offer, details_data):
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)


class OfferDetailListSerializer(serializers.ModelSerializer):
    """Serialize the identifier URL of an offer detail."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = [
            'id', 'url'
        ]

    def get_url(self, obj):
        """Build the relative API URL for an offer detail."""
        return f"/offerdetails/{obj.id}/"


class UserDetailSerializer(serializers.ModelSerializer):
    """Serialize the public identity fields of an offer owner."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class OfferListSerializer(serializers.ModelSerializer):
    """Serialize an offer for list responses with summary values."""

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
        """Return the lowest price among the offer's tiers."""
        result = obj.details.aggregate(Min("price"))
        return result['price__min']

    def get_min_delivery_time(self, obj):
        """Return the shortest delivery time among the offer's tiers."""
        result = obj.details.aggregate(Min("delivery_time_in_days"))
        return result['delivery_time_in_days__min']


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """Serialize an offer for detail responses."""
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
        """Return the lowest price among the offer's tiers."""
        result = obj.details.aggregate(Min("price"))
        return result['price__min']

    def get_min_delivery_time(self, obj):
        """Return the shortest delivery time among the offer's tiers."""
        result = obj.details.aggregate(Min("delivery_time_in_days"))
        return result['delivery_time_in_days__min']


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Validate and update an offer and its nested pricing tiers."""

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['title', 'details']

    def update(self, instance, validated_data):
        """Update the offer and matching tiers by offer type."""
        details_data = validated_data.pop('details', None)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        if details_data:
            self._update_details(instance, details_data)
        return instance

    def _update_details(self, instance, details_data):
        details = instance.details.all()
        for detail_data in details_data:
            detail = details.get(offer_type=detail_data.get('offer_type'))
            self._update_detail(detail, detail_data)

    def _update_detail(self, detail, detail_data):
        editable_fields = ('title', 'revisions', 'delivery_time_in_days',
                           'price', 'features')
        for field in editable_fields:
            setattr(detail, field, detail_data.get(field, getattr(detail, field)))
        detail.save()

    def validate_details(self, value):
        """Ensure every submitted tier identifies its offer type."""
        for detail in value:
            if 'offer_type' not in detail:
                raise serializers.ValidationError("Each detail must include an offer_type.")
        return value