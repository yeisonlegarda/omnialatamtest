from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from principal.models import Payment
from ecomerce.serializers import PaymentEntireSerializer
from ecomerce.tests.test_product import create_product
from ecomerce.tests.test_orders import create_order

PAYMENTS_URL = reverse('product:payment-list')


def detail_url(payment_id):
    """Return product detail URL"""
    return reverse('product:payment-detail', args=[payment_id])


def create_payment(**params):
    """Create and return a sample payment"""
    defaults = {
        'value': 1500.25,
    }
    defaults.update(params)
    return Payment.objects.create(**defaults)


class PublicPaymentApiTest(TestCase):
    """Test authenticated need for payment operations"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required for payment operations"""
        res = self.client.get(PAYMENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePaymentApiTest(TestCase):
    """Test authenticated payment operations"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_payments_limited_to_user(self):
        """"test that orders retrieved belongs to user"""
        user2 = get_user_model().objects.create_user(
            "other@email.com"
            'password123'
        )
        create_payment(user=user2)
        create_payment(user=self.user)

        res = self.client.get(PAYMENTS_URL)

        payments = Payment.objects.filter(user=self.user)
        serializer = PaymentEntireSerializer(payments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_create_payment_with_orders(self):
        """Test create payment with embeeded order"""
        prod1 = create_product(name="Testpr1")
        prod2 = create_product(name="Testpr2")
        order = create_order(user=self.user)
        order.products.add(prod1, prod2)

        payload = {
            'value': 150.23,
            'orders': [order.id],
        }
        res = self.client.post(PAYMENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        payment = Payment.objects.get(id=res.data['id'])
        orders = payment.orders.all()
        self.assertEqual(orders.count(), 1)
        self.assertIn(order, orders)

    def test_partial_update_order(self):
        """Test partial update over payment"""
        order = create_order(user=self.user)
        order.products.add(create_product())
        payment = create_payment(user=self.user)
        payment.orders.add(order)
        new_order = create_order(user=self.user)
        new_order.products.add(create_product(name="test product new"))

        payload = {'orders': [new_order.id]}
        url = detail_url(payment.id)
        self.client.patch(url, payload)

        payment.refresh_from_db()
        orders = payment.orders.all()
        self.assertEqual(len(orders), 1)
        self.assertIn(new_order, orders)
