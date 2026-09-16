from django.contrib.auth.models import User
from users_app.models import UserProfile
from django.urls import reverse
from django.test import TestCase

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status

from reviews_app.models import Review


class ReviewBaseTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='max@test.de',
            password='Test12345!'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,  type='customer')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('reviews')
        self.business_user = User.objects.create_user(
            username='businessuser',
            email='business@test.de',
            password='Test12345!'
        )
        self.business_profile = UserProfile.objects.create(
            user=self.business_user,  type='business')
        self.business_token, _ = Token.objects.get_or_create(
            user=self.business_user)
        self.valid_data = {
            'business_user': self.business_user.pk,
            'rating': 5,
            'description': 'Very good service.'
        }


class ReviewCreateHappyTest(ReviewBaseTestCase):
    def test_create_review_success(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

        review = Review.objects.first()
        self.assertEqual(review.business_user, self.business_user)
        self.assertEqual(review.reviewer, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.description, 'Very good service.')


class ReviewCreateUnHappyTest(ReviewBaseTestCase):

    def test_create_review_invalid_rating(self):
        self.valid_data['rating'] = 6
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_unauthenticated(self):
        self.client.credentials()
        response = self.client.post(self.url,  self.valid_data,  format='json')
        self.assertEqual(response.status_code,  status.HTTP_401_UNAUTHORIZED)

    def test_create_review_as_business_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response = self.client.post(
            self.url,   self.valid_data,  format='json')
        self.assertEqual(response.status_code,  status.HTTP_403_FORBIDDEN)


class ReviewListHappyTestCase(ReviewBaseTestCase):

    def test_get_review_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewListUnHappyTestCase(ReviewBaseTestCase):

    def test_get_reviews_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,  status.HTTP_401_UNAUTHORIZED)


class ReviewPatchHappyTestCase(ReviewBaseTestCase):
    def test_patch_review_success(self):
        review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.user,
            rating=5,
            description='Very good service.'
        )
        self.url = reverse('review-detail', kwargs={'pk': review.pk})
        self.data = {'rating': 4, 'description': 'Noch besser als erwartet!'}
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewPatchUnHappyTestCase(ReviewBaseTestCase):

    def test_patch_review_invalid_data(self):
        review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.user,
            rating=5,
            description='Very good service.')
        self.url = reverse('review-detail', kwargs={'pk': review.pk})
        self.data = {'rating': 6,  'description': 'Invalid rating'}
        response = self.client.patch(self.url, self. data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_review_unauthenticated(self):
        review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.user,
            rating=5,
            description='Very good service.'
        )
        self.url = reverse('review-detail', kwargs={'pk': review.pk})
        self.client.credentials()
        self.data = {'rating': 4,  'description': 'Updated review'}
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_review_not_owner(self):
        review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.user,
            rating=5,
            description='Very good service.'
        )
        self.url = reverse('review-detail', kwargs={'pk': review.pk})
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        self.data = {'rating': 4,   'description': 'Updated review'}
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_review_not_found(self):
        self.url = reverse('review-detail', kwargs={'pk': 99999})
        self.data = {'rating': 4,   'description': 'Updated review'}
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
