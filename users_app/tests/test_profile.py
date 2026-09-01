from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from users_app.models import UserProfile
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class ProfileHappyTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.de',
            password='Test12345!')

        self.profile = UserProfile.objects.create(
            user=self.user,
            type='customer'
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_profile_with_valid_user_id(self):
        url = reverse('profile', kwargs={'pk': self.user.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@test.de')
        self.assertEqual(response.data['type'], 'customer')
        self.assertEqual(response.data['file'], '')

    def test_patch_own_profile(self):
        url = reverse('profile', kwargs={'pk': self.user.id})
        data = {
            'first_name': 'Max',
            'last_name': 'Mustermann',
            'location': 'Berlin',
            'email': 'max@test.de'
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(self.user.first_name, 'Max')
        self.assertEqual(self.user.last_name, 'Mustermann')
        self.assertEqual(self.user.email, 'max@test.de')
        self.assertEqual(self.profile.location, 'Berlin')


class ProfileUnhappyTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@test.de',
            password='Test12345!')

        self.profile = UserProfile.objects.create(
            user=self.user,
            type='customer'
        )

        self.client = APIClient()

    def test_get_profile_unauthenticated(self):
        url = reverse('profile', kwargs={'pk': self.user.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('profile', kwargs={'pk': 999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'User profile not found.')

    def test_patch_profile_unauthenticated(self):
        url = reverse('profile', kwargs={'pk': self.user.id})
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_other_user_profile_forbidden(self):
        other_user = User.objects.create_user(
            username='otheruser',
            email='otheruser@test.de',
            password='Test12345!')

        other_profile = UserProfile.objects.create(
            user=other_user,
            type='customer'
        )
        self.client.force_authenticate(user=self.user)
        url = reverse('profile', kwargs={'pk': other_user.id})
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'], 'You do not have permission to update this profile.')

    def test_patch_profile_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('profile', kwargs={'pk': 999})
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'User profile not found.')
