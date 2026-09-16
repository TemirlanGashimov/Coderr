from reviews_app.models import Review
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):

    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def validate_business_user(self, value):
        if value.profile.type != "business":
            raise serializers.ValidationError(
                "User must have a business profile.")
        return value

    def validate(self, attrs):

        if Review.objects.filter(reviewer=self.context['request'].user, business_user=attrs['business_user']).exists():
            raise serializers.ValidationError("You have already reviewed this business user.")
        return attrs

class ReviewUpdateSerializer(serializers.ModelSerializer):

    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['rating', 'description']