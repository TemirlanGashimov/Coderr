from django.contrib.auth.models import User
from users_app.models import UserProfile
from django.urls import reverse
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status

from offers_app.models import Offer, OfferDetail


class OfferBaseTestCase(TestCase):

    user_type = 'business'

    def setUp(self):
        self.user = User.objects.create_user(
            username='businessuser',
            email='business@test.de',
            password='Test12345!'
        )

        self.profile = UserProfile.objects.create(
            user=self.user, type=self.user_type)
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('offers')
        self.valid_data = {
            'title': 'Grafikdesign-Paket',
            'description': 'Ein Testangebot',
            'details': [
                {
                    'title': 'Basic Design',
                    'revisions': 2,
                    'delivery_time_in_days': 5,
                    'price': 100,
                    'features': ['Logo Design'],
                    'offer_type': 'basic'
                },
                {
                    'title': 'Standard Design',
                    'revisions': 5,
                    'delivery_time_in_days': 7,
                    'price': 200,
                    'features': ['Logo Design', 'Visitenkarte'],
                    'offer_type': 'standard'
                },
                {
                    'title': 'Premium Design',
                    'revisions': 10,
                    'delivery_time_in_days': 10,
                    'price': 500,
                    'features': ['Logo Design', 'Visitenkarte', 'Flyer'],
                    'offer_type': 'premium'
                }
            ]
        }


class OfferPostHappyTestCase(OfferBaseTestCase):

    def test_post_create_offer(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(OfferDetail.objects.count(), 3)

        offer = Offer.objects.first()
        self.assertEqual(offer.user, self.user)


class OfferGetHappyTestCase(OfferBaseTestCase):

    def test_get_offers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offers_by_creator_id(self):
        offer = Offer.objects.create(
            user=self.user, title='Test Offer', description='Test Beschreibung')
        response = self.client.get(self.url, {'creator_id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], offer.id)

    def test_get_offer_by_min_price(self):
        offer = Offer.objects.create(
            user=self.user, title='Test Offer', description='Test Beschreibung')

        OfferDetail.objects.create(
            offer=offer, title='Basic Design', revisions=2, delivery_time_in_days=5,
            price=50, features=['Logo Design'], offer_type='basic')

        response = self.client.get(self.url, {'min_price': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_get_offer_by_max_delivery_time(self):
        offer = Offer.objects.create(
            user=self.user, title='Test Offer', description='Test Beschreibung')

        OfferDetail.objects.create(
            offer=offer, title='Basic Design', revisions=2,
            delivery_time_in_days=10, price=100, features=['Logo Design'], offer_type='basic')

        response = self.client.get(self.url, {'max_delivery_time': 7})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_get_offer_by_search(self):
        offer = Offer.objects.create(
            user=self.user, title='Grafik Design', description='Test Beschreibung')

        response = self.client.get(self.url, {'search': 'Grafik'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], offer.id)

    def test_get_offers_ordered_by_min_price(self):
        offer_expensive = Offer.objects.create(
            user=self.user, title='Expensive Offer', description='Test')
        OfferDetail.objects.create(offer=offer_expensive, title='Expensive Detail',
                                   revisions=1, delivery_time_in_days=5, price=200, features=[], offer_type='basic')

        offer_cheap = Offer.objects.create(
            user=self.user, title='Cheap Offer', description='Test')
        OfferDetail.objects.create(offer=offer_cheap, title='Cheap Detail', revisions=1, delivery_time_in_days=5,
                                   price=50, features=[], offer_type='basic')

        response = self.client.get(self.url, {'ordering': 'min_price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['id'], offer_cheap.id)
        self.assertEqual(response.data['results'][1]['id'], offer_expensive.id)


class OfferRetrieveGetHappyTestCase(OfferBaseTestCase):

    def test_get_offers_pk(self):
        offer = Offer.objects.create(
            user=self.user, title='Test Offer', description='Test Beschreibung')
        self.url = reverse("offer", kwargs={"pk": offer.pk})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], offer.pk)


class OfferPostUnhappyTestCase(OfferBaseTestCase):

    def test_post_offer_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_cannot_create_offer(self):
        self.profile.type = 'customer'
        self.profile.save()
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offer_requires_three_details(self):
        invalid_data = self.valid_data.copy()
        invalid_data['details'] = self.valid_data['details'][:2]
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_requires_basic_standard_premium(self):
        invalid_data = self.valid_data.copy()
        invalid_data['details'] = [detail.copy()
                                   for detail in self.valid_data['details']]
        invalid_data['details'][2]['offer_type'] = 'standard'
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OfferGetUnHappyTestCase(OfferBaseTestCase):

    def test_get_offers_unauthenticated(self):
        self.client.credentials()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class OfferRetrieveGetUnHappyTestCase(OfferBaseTestCase):

    def test_get_offers_pk_unathenticated(self):
        offer = Offer.objects.create(
            user=self.user, title='Test Offer', description='Test Beschreibung')
        self.client.credentials()
        self.url = reverse("offer", kwargs={"pk": offer.pk})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offer_pk_not_found(self):
        self.url = reverse("offer", kwargs={"pk": 99999})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)