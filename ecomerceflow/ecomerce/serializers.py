from rest_framework import serializers
from principal.models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for products saving and retrieves"""

    class Meta:
        model = Product
        fields = ("id", "name", "price", "stockQuantity")
        read_only_fields = ("id",)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders created"""

    class Meta:
        model = Order
        fields = ("id", "products", "orderDate")
        read_only_fields = ("id",)

class OrderEntireSerializer(OrderSerializer):
    """Serializes object for retrieve operations"""
    products = ProductSerializer(many=True, read_only=True)
