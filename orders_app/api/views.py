from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from orders_app.models import Order

from .permissions import IsCustomer, IsBusiness
from .filters import orders_for_business_user, orders_for_user
from .serializers import OrderSerializer, OrderStatusSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    """List a user's orders or create an order as a customer."""
    queryset = Order.objects.all()
    permission_classes = [IsCustomer, IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = None

    def get_queryset(self):
        """Return orders where the requester is customer or business user."""
        return orders_for_user(self.request.user)

    def get_permissions(self):
        """Require authentication for reads and customer access for creates."""
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsCustomer(), IsAuthenticated()]


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Read or update orders and allow administrators to delete them."""
    queryset = Order.objects.all()
    serializer_class = OrderStatusSerializer
    permission_classes = [IsBusiness, IsAuthenticated]

    def get_permissions(self):
        """Use administrator access for deletion and business access otherwise."""
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        else:
            return [IsBusiness(), IsAuthenticated()]


class OrderCountAPIView(generics.GenericAPIView):
    """Return the number of in-progress orders for a business user."""
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """Count in-progress orders after validating the business profile."""
        business_user = get_object_or_404(User, pk=business_user_id)
        if business_user.profile.type != 'business':
            raise NotFound()
        order_count = orders_for_business_user(
            business_user, 'in_progress').count()
        return Response({"order_count": order_count})


class OrderCountCompletedAPIView(generics.GenericAPIView):
    """Return the number of completed orders for a business user."""
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        """Count completed orders after validating the business profile."""
        business_user = get_object_or_404(User, pk=business_user_id)
        if business_user.profile.type != 'business':
            raise NotFound()
        completed_order_count = orders_for_business_user(
            business_user, 'completed').count()
        return Response({'completed_order_count': completed_order_count})
