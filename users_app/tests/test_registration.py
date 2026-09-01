from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


# HAPPY CASE

class RegistrationHappyTestCase(TestCase):

    def setUp(self):
        self.url = reverse('registration')
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@test.de',
            'password': 'Test12345!',
            'repeated_password': 'Test12345!',
            'type': 'customer'
        }

    def test_post_registration_with_valid_data(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@test.de')
        self.assertIn('user_id', response.data)


class RegistrationUnhappyTestCase(TestCase):

    def setUp(self):
        self.url = reverse('registration')

        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@test.de',
            'password': 'Test12345!',
            'repeated_password': 'Test12345!',
            'type': 'customer'
        }

    def test_post_registration_with_different_passwords(self):
        self.valid_data['repeated_password'] = 'WrongPassword123!'

        response = self.client.post(
            self.url,
            self.valid_data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_post_registration_with_existing_email(self):
        User.objects.create_user(
            username='existinguser',
            email='testuser@test.de',
            password='Test12345!'
        )

        response = self.client.post(
            self.url,
            self.valid_data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_post_registration_with_existing_username(self):
        User.objects.create_user(
            username='testuser',
            email='other@test.de',
            password='Test12345!'
        )

        response = self.client.post(
            self.url,
            self.valid_data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_post_registration_with_invalid_type(self):
        self.valid_data['type'] = 'admin'

        response = self.client.post(
            self.url,
            self.valid_data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
