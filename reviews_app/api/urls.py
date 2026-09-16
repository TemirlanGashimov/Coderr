from django.urls import path
from .views import ReviewListCreateAPIView

urlpatterns = [
    path('review/', ReviewListCreateAPIView.as_view(), name='review'),
]