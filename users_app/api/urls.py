from django.urls import path
from .views import RegistrationAPIView, LoginAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
