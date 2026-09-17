from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers

from users_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate and create a user with a marketplace profile."""

    repeated_password = serializers.CharField(write_only=True)

    type = serializers.ChoiceField(
        choices=UserProfile.TYPE_CHOICES, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        """Validate matching passwords and unique email addresses."""
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "Email is already in use."}
            )

        return attrs

    def create(self, validated_data):
        """Create the Django user and its selected profile type."""
        user_type = validated_data.pop('type')
        validated_data.pop('repeated_password')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, type=user_type)
        return user


class LoginSerializer(serializers.Serializer):
    """Authenticate a user with username and password credentials."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Authenticate the submitted credentials."""
        user = authenticate(
            username=attrs['username'], password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError(
                {"detail": "Invalid credentials."}
            )
        attrs['user'] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    """Serialize a complete public user profile."""

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    created_at = serializers.DateTimeField(
        source='user.date_joined', read_only=True)
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        """Return the profile file URL when a file exists."""
        if not obj.file:
            return ""
        return obj.file.url

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location',
                  'tel', 'description', 'working_hours', 'type', 'email', 'created_at']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Validate and update editable profile and user fields."""

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    def update(self, instance, validated_data):
        """Update profile fields and the related Django user."""
        user_data = validated_data.pop('user', {})
        self._update_user(instance.user, user_data)
        self._update_profile(instance, validated_data)
        instance.user.save()
        instance.save()
        return instance

    def _update_user(self, user, user_data):
        for field in ('last_name', 'first_name', 'email'):
            setattr(user, field, user_data.get(field, getattr(user, field)))

    def _update_profile(self, instance, validated_data):
        fields = ('location', 'tel', 'description', 'working_hours')
        for field in fields:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'location',
                  'tel', 'description', 'working_hours', 'email']


class BusinessProfileSerializer(serializers.ModelSerializer):
    """Serialize public business profile information."""

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        """Return the profile file URL when a file exists."""
        if not obj.file:
            return ""
        return obj.file.url

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'type']


class CustomerProfileSerializer(serializers.ModelSerializer):
    """Serialize public customer profile information."""

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        """Return the profile file URL when a file exists."""
        if not obj.file:
            return ""
        return obj.file.url

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name',
                  'last_name', 'file', 'uploaded_at', 'type']
