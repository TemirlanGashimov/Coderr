from django.urls import path
from .views import ReviewListCreateAPIView, ReviewDetailAPIView

urlpatterns = [
    path('reviews/', ReviewListCreateAPIView.as_view(), name='reviews'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(),name='review-detail')
]