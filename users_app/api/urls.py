from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, ProfileAPIView, BusinessProfileListAPIView, CustomerProfileListAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileAPIView.as_view(), name='profile'),
    path('profiles/business/', BusinessProfileListAPIView.as_view(), name='business-profiles'),
    path('profiles/customer/', CustomerProfileListAPIView.as_view(), name='customer-profiles')
]
