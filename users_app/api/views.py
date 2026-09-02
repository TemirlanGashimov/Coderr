from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users_app.models import UserProfile
from rest_framework.permissions import IsAuthenticated

from users_app.api.serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer, ProfileUpdateSerializer, BusinessProfileSerializer, CustomerProfileSerializer


class RegistrationAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

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


class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

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


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user_profile = UserProfile.objects.get(user__id=pk)
            serializer = ProfileSerializer(user_profile)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            user_profile = UserProfile.objects.get(user__id=pk)

            if request.user.id != pk:
                return Response(
                    {"detail": "You do not have permission to update this profile."},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = ProfileUpdateSerializer(
                user_profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                response_serializer = ProfileSerializer(user_profile)

                return Response(response_serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)


class BusinessProfileListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        business_profiles = UserProfile.objects.filter(type='business')
        serializer = BusinessProfileSerializer(business_profiles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerProfileListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer_profiles = UserProfile.objects.filter(type='customer')
        serializer = CustomerProfileSerializer(customer_profiles, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
