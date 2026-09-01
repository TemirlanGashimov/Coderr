from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, ProfileAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileAPIView.as_view(), name='profile'),
]
