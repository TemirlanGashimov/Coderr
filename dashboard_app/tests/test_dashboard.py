from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


class BaseInfoHappyTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('base-info')

    def test_base_info_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)