from django.contrib.auth.models import User
from orders_app.models import Order
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsCustomer, IsBusiness
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound

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

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        else:
            return [IsBusiness(), IsAuthenticated()]

class OrderCountAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, pk=business_user_id)
        if business_user.profile.type != 'business':
            raise NotFound()
        order_count = Order.objects.filter(business_user=business_user, status='in_progress').count()
        return Response({"order_count": order_count})