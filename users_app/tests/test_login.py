from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from django.test import TestCase


class LoginHappyTestCase(TestCase):

    def setUp(self):
        self.url = reverse('login')

        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.de',
            password='Test12345!'
        )

        self.valid_data = {
            'username': 'testuser',
            'password': 'Test12345!'
        }

    def test_post_login_with_valid_data(self):
        response = self.client.post(self.url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@test.de')
        self.assertEqual(response.data['user_id'], self.user.id)


class LoginUnhappyTestCase(TestCase):

    def setUp(self):
        self.url = reverse('login')

        User.objects.create_user(
            username='testuser',
            email='testuser@test.de',
            password='Test12345!'
        )

    def test_post_login_with_wrong_password(self):
        data = {
            'username': 'testuser',
            'password': 'WrongPassword!'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_login_with_unknown_username(self):
        data = {
            'username': 'unknownuser',
            'password': 'Test12345!'
        }

        response = self.client.post(self.url,  data,  format='json')

        self.assertEqual(response.status_code,  status.HTTP_400_BAD_REQUEST)

    def test_post_login_without_username(self):
        data = {
            'password': 'Test12345!'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_login_without_password(self):
        data = {
            'username': 'testuser'
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
