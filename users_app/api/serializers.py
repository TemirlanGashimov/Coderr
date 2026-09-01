from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from users_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)

    type = serializers.ChoiceField(
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

        if User.objects.filter(email=attrs['email']).exists():
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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
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

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    created_at = serializers.DateTimeField(source='user.date_joined', read_only=True)#
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        if not obj.file:
            return ""
        return obj.file.url

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location',
                  'tel', 'description', 'working_hours', 'type', 'email', 'created_at']


class ProfileUpdateSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        instance.location = validated_data.get('location', instance.location)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.description = validated_data.get('description', instance.description)
        instance.working_hours = validated_data.get('working_hours', instance.working_hours)
        instance.user.email = user_data.get('email', instance.user.email)

        instance.user.save()
        instance.save()
        return instance

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours', 'email']

