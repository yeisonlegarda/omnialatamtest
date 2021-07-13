from rest_framework import mixins, status
from rest_framework.viewsets import ModelViewSet
from ecomerce.serializers import ProductSerializer, OrderSerializer, \
    OrderEntireSerializer, PaymentSerializer, PaymentEntireSerializer, \
    ShipmentSerializer, ShipmentEntireSerializer
from principal.models import Product, Order, Payment, Shipment
import asyncio
from principal.services.EmailSender import send_email


class ProductsViewSet(ModelViewSet):
    """Manages products on database"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class OrderViewSet(ModelViewSet):
    """Manage orders on database """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        """Return objects for the current authenticated user"""
        return self.queryset.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """"Return appropriate serializer class"""
        if self.action in ['retrieve', 'list']:
            return OrderEntireSerializer
        return self.serializer_class


class PaymentViewSet(ModelViewSet):
    """Manage orders on database """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_queryset(self):
        """Return objects for the current authenticated user"""
        return self.queryset.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """"Return appropriate serializer class"""
        if self.action in ['retrieve', 'list']:
            return PaymentEntireSerializer
        return self.serializer_class


class ShipmentViewSet(ModelViewSet):
    """Manage shipments on database """
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()

    def get_queryset(self):
        """Return objects for the current authenticated user"""
        return self.queryset.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        asyncio.run(send_email(self.request))

    def get_serializer_class(self):
        """"Return appropriate serializer class"""
        if self.action in ['retrieve', 'list']:
            return ShipmentEntireSerializer
        return self.serializer_class
