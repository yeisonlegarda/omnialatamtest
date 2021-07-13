from django.test import TestCase
from django.contrib.auth import get_user_model
from principal import models


class ModelTest(TestCase):

    def test_user_email_creation(self):
        """Test new user creation"""
        email = "user@email.com"
        password = 'Testpassword'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)

    def test_user_bad_email(self):
        """Test for creating an user not email set"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'TestPassword')

    def test_super_user_creation(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_superuser(
            email='user@email.com',
            password='Testpassword'
        )
        self.assertTrue(user.is_superuser)

    def test_product(self):
        """test product model creation and str conversion"""
        product = models.Product.objects.create(
            name='TestProduct',
            price=50000,
        )
        self.assertIn(product.name,str(product))
        self.assertEqual(product.stockQuantity,0)

    def test_order(self):
        """test product model creation and str conversion"""
        product = models.Product.objects.create(
            name='TestProduct',
            price=50000,
        )
        self.assertIn(product.name,str(product))
        self.assertEqual(product.stockQuantity,0)
