from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from principal.models import Order
from ecomerce.serializers import OrderEntireSerializer
from ecomerce.tests.test_product import create_product


ORDERS_URL = reverse('product:order-list')


def create_order(**params):
    """Create and return an order"""
    return Order.objects.create(**params)

def detail_url(order_id):
    """Return product detail URL"""
    return reverse('product:order-detail', args=[order_id])


class PublicOrdersApiTest(TestCase):
    """Test authenticated need for order operations"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required for product operations"""
        res = self.client.get(ORDERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderApiTest(TestCase):
    """Test authenticated Order operations"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_orders_limited_to_user(self):
        """"test that orders retrieved belongs to user"""
        user2 = get_user_model().objects.create_user(
            "other@email.com"
            'password123'
        )
        create_order(user=user2)
        create_order(user=self.user)

        res = self.client.get(ORDERS_URL)

        orders = Order.objects.filter(user=self.user)
        serializer = OrderEntireSerializer(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_create_order_with_products(self):
        """Test create order with embeeded products"""
        prod1 = create_product(name="Testpr1")
        prod2 = create_product(name="Testpr2")
        payload = {
            'products': [prod1.id, prod2.id],
        }
        res = self.client.post(ORDERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=res.data['id'])
        products = order.products.all()
        self.assertEqual(products.count(), 2)
        self.assertIn(prod1, products)
        self.assertIn(prod2, products)

    def test_partial_update_order(self):
        """Test partial update over order"""
        order = create_order(user=self.user)
        order.products.add(create_product())
        new_product = create_product(name='test product 1')

        payload = {'products': [new_product.id]}
        url = detail_url(order.id)
        self.client.patch(url, payload)

        order.refresh_from_db()
        products = order.products.all()
        self.assertEqual(len(products), 1)
        self.assertIn(new_product, products)
