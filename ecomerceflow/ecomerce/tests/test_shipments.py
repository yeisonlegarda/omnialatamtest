from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from principal.models import Shipment
from ecomerce.serializers import ShipmentEntireSerializer
from ecomerce.tests.test_product import create_product
from ecomerce.tests.test_orders import create_order
from django.core import mail
import time

SHIPMENTS_URL = reverse('product:shipment-list')


def detail_url(shipment_id):
    """Return product detail URL"""
    return reverse('product:shipment-detail', args=[shipment_id])


def create_shipment(**params):
    """Create and return a sample shipment"""
    defaults = {
        'sent_date': "2021-07-12T00:00:00.00Z",
    }
    defaults.update(params)
    return Shipment.objects.create(**defaults)


class PublicShipmenApiTest(TestCase):
    """Test authenticated need for payment operations"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required for shipment operations"""
        res = self.client.get(SHIPMENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateShipmenApiTest(TestCase):
    """Test authenticated shipment operations"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_shipments_limited_to_user(self):
        """"test that shipments retrieved belongs to user"""
        user2 = get_user_model().objects.create_user(
            "other@email.com"
            'password123'
        )
        order = create_order(user=self.user)
        order.products.add(create_product())
        create_shipment(user=user2, order=order)
        create_shipment(user=self.user, order=order)

        res = self.client.get(SHIPMENTS_URL)

        shipments = Shipment.objects.filter(user=self.user)
        serializer = ShipmentEntireSerializer(shipments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_mail_sent_on_create(self):
        """Test sent mail on post call mail outbox after 5 attemps stops
        if not mail in that time breaks loops and gives try like error"""
        order = create_order(user=self.user)
        payload = {
            "sent_date": "2021-07-12T0:0:0.0Z",
            "order": order.id,
            "user": self.user.id,
        }
        response = self.client.post(SHIPMENTS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        counter_attempts = 0
        while True:
            if counter_attempts > 4 or len(mail.outbox) > 0:
                break
            time.sleep(0.005)
            counter_attempts += 1
        self.assertEqual(len(mail.outbox), 1)
