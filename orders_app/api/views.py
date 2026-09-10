from orders_app.models import Order
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomer, IsBusiness
from django.db.models import Q

from .serializers import OrderSerializer, OrderStatusSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsCustomer, IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user))
        return orders

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else: 
            return [IsCustomer(), IsAuthenticated()]

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [IsBusiness, IsAuthenticated]