from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.exceptions import NotFound, PermissionDenied
from users_app.models import UserProfile
from rest_framework.permissions import IsAuthenticated

from users_app.api.serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer, BusinessProfileSerializer, CustomerProfileSerializer


class RegistrationAPIView(generics.CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()

            token, _ = Token.objects.get_or_create(user=saved_account)

            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id,
            }

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)

            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            user_profile = self.get_queryset().get(user__id=self.kwargs['pk'])

        except UserProfile.DoesNotExist:
            raise NotFound("User profile not found.")

        if self.request.method == 'PATCH' and self.request.user.id != self.kwargs['pk']:
            raise PermissionDenied(
                "You do not have permission to update this profile."
            )
        return user_profile

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return ProfileUpdateSerializer
        return ProfileSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_serializer = ProfileSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class BusinessProfileListAPIView(generics.ListAPIView):
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(type='business')


class CustomerProfileListAPIView(generics.ListAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(type='customer')
