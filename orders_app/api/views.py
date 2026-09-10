from orders_app.models import Order
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomer

from .serializers import OrderSerializer

class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsCustomer, IsAuthenticated]
    serializer_class = OrderSerializer

