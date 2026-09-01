from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from users_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):

    repeat_password = serializers.CharField(write_only=True)
    type = serializers.ChoisField(
        choices=UserProfile.TYPE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        
        if User.object.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email is already in use."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user_type = validated_data.pop('type')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        UserProfile.objects.create(
            user=user,
            type=user_type
        )
        return user
