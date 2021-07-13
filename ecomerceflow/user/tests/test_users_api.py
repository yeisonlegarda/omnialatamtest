from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Creates user on db directly"""
    return get_user_model().objects.create_user(**params)


class ClientAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test creating an user with valid payload, retrieves no password and
         password its same"""
        payload = {
            'email': 'tes@email.com',
            'password': 'Testpassword',
            'name': 'Test user',
            'address': 'test address'
        }
        resp = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        userdb = get_user_model().objects.get(**resp.data)
        self.assertTrue(userdb.check_password(payload['password']))
        self.assertNotIn('password', resp.data)

    def test_create_existing_user(self):
        """Test to look up for existing user creation cannot be performed"""
        payload = {
            'email': 'tes@email.com',
            'password': 'Testpassword',
            'name': 'Test user'
        }
        create_user(**payload)
        resp = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test user cannot be created if too short password"""
        payload = {
            'email': 'testunexinting@email.com',
            'password': '1',
            'name': 'Test user'
        }
        resp = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.all(). \
            filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_token_creation(self):
        """Test token creation"""
        payload = {'email': 'testuser@email.com', 'password': 'testpass'}
        create_user(**payload)
        resp = self.client.post(TOKEN_URL, payload)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertIn('token', resp.data)

    def test_bad_credentials(self):
        """Test token no retrieved for invalid credentials"""
        create_user(email='testuser@email.com',password='testpass')
        payload = {'email': 'testuser@email.com', 'password': 'testpassInv'}
        resp = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token',resp.data)
        self.assertEqual(resp.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test don't retrieve token if doesn't user exist on db"""
        payload = {'email': 'testuser@email.com', 'password': 'testpassInv'}
        resp = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_provided_field(self):
        """Test don't retrieve token if missing field on auth"""
        payload = {'email': 'testuser@email.com', 'password': ''}
        resp = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
