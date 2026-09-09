from django.urls import path
from .views import OfferListCreateAPIView, OfferRetrieveUpdateDestroyAPIView, OfferDetailRetrieveAPIView

urlpatterns = [
    path('offers/', OfferListCreateAPIView.as_view(), name='offers'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyAPIView.as_view(), name='offer'),
    path('offerdetails/<int:pk>/', OfferDetailRetrieveAPIView.as_view(), name='offer-detail')
]