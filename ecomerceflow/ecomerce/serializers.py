from rest_framework import serializers
from principal.models import Product, Order, Payment, Shipment

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


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payments creation,update"""

    class Meta:
        model = Payment
        fields = ("id", "value", "date", "orders")
        read_only_fields = ("id",)


class PaymentEntireSerializer(PaymentSerializer):
    """Serializes object for retrieve operations over payments"""
    orders = OrderSerializer(many=True, read_only=True)

class ShipmentSerializer(serializers.ModelSerializer):
    """Serializer for shipment creation,update"""

    class Meta:
        model = Shipment
        fields = ("id", "sent_date", "received_date", "order","user")
        read_only_fields = ("id",)

class ShipmentEntireSerializer(ShipmentSerializer):
    """Serializes object for retrieve operations over payments"""
    order = OrderSerializer(read_only=True)
