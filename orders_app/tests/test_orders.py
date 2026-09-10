from django.contrib.auth.models import User
from users_app.models import UserProfile
from django.urls import reverse
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class OrderBaseTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='max@test.de',
            password='Test12345!'
        )
        self.profile = UserProfile.objects.create(
            user=self.user, type='customer')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('orders')
        self.business_user = User.objects.create_user(
            username='businessuser',
            email='business@test.de',
            password='Test12345!'
        )
        self.business_profile = UserProfile.objects.create(
            user=self.business_user, type='business')

        self.offer = Offer.objects.create(
            user=self.business_user, title='Test Offer', description='Test Beschreibung')

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer, title="Logo Design", revisions=3, delivery_time_in_days=5,
            price=10, features=['Logo Design'], offer_type="basic")

        self.valid_data = {"offer_detail_id": self.offer_detail.pk}


class OrderCreateHappyTestCase(OrderBaseTestCase):

    def test_post_order(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.exists())

        order = Order.objects.get(customer_user=self.user, title=self.offer_detail.title)
        self.assertEqual(order.title, self.offer_detail.title)


class OrderCreateUnHappyTestCase(OrderBaseTestCase):

    def test_post_order_without_offer_detail_id(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_order_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_order_forbidden_for_business_user(self):
        self.profile.type = 'business'
        self.profile.save()
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_order_offer_detail_not_found(self):
        invalid_data = ({'offer_detail_id': 99999})
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)