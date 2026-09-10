from django.urls import path
from .views import OrderListCreateAPIView, OrderDetailAPIView

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail')
]