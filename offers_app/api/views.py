from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from . serializers import OfferSerializer


class OfferListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.profile.type != 'business':
            return Response(
                {"detail": "Only business users can create offers."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = OfferSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(
                serializer.data,status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,status=status.HTTP_400_BAD_REQUEST
        )