from rest_framework import serializers
from offers_app.models import OfferDetail, Offer


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
            'id','title', 'image', 'description', 'details'
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
