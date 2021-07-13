from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from principal.models import Product
from ecomerce.serializers import ProductSerializer

PRODUCTS_URL = reverse('product:product-list')


def create_product(**params):
    """Create and return a sample product"""
    defaults = {
        'name': 'Test product',
        'stockQuantity': 10,
        'price': 1500.52
    }
    defaults.update(params)
    return Product.objects.create(**defaults)


def detail_url(product_id):
    """Return product detail URL"""
    return reverse('product:product-detail', args=[product_id])


class PublicProductApiTest(TestCase):
    """Test authenticated need for products operations"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required for product operations"""
        res = self.client.get(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductApiTest(TestCase):
    """Test authenticated recipe"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@email.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieveing recipes"""
        create_product()
        create_product()

        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_product_detail(self):
        """Test viewing a product detail"""
        product = create_product()

        url = detail_url(product.id)
        res = self.client.get(url)

        serializer = ProductSerializer(product)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        """Test create a product"""
        payload = {
            'name': 'test product',
            'price': 150.2,
            'stockQuantity': 50
        }
        res = self.client.post(PRODUCTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=res.data['id'])
        serializer = ProductSerializer(product)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update_product(self):
        """Test partial update over product"""
        product = create_product()

        payload = {'name': 'product 2'}
        url = detail_url(product.id)

        self.client.patch(url, payload)

        product.refresh_from_db()

        self.assertEqual(product.name, payload['name'])

    def test_full_update_product(self):
        """Test updating a recipe with put"""
        product = create_product()
        payload = {
            'name': 'test product 2',
            'price': 15.25,
            'stockQuantity': 50
        }
        url = detail_url(product.id)
        self.client.put(url, payload)

        product.refresh_from_db()
        self.assertEqual(product.name, payload['name'])
        self.assertEqual(product.price, payload['price'])
        self.assertEqual(product.stockQuantity, payload['stockQuantity'])

    def test_product_pagination(self):
        """Test pagination over product query"""
        products = []
        limit = 2
        products.append(create_product(name="test product"))
        products.append(create_product(name="test product 2"))
        products.append(create_product(name="test product 3"))
        products.append(create_product(name="test product 4"))
        products.append(create_product(name="test product 5"))
        res = self.client.get(PRODUCTS_URL, {'limit': limit, 'offset': 0})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), limit)
        self.assertTrue(res.data['previous'] is None)
        self.assertFalse(res.data['next'] is None)