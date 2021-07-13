from ecomerce.views import ProductsViewSet, OrderViewSet, \
    PaymentViewSet, ShipmentViewSet
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('products',ProductsViewSet)
router.register('orders',OrderViewSet)
router.register('payments',PaymentViewSet)
router.register('shipments',ShipmentViewSet)

app_name = 'product'

urlpatterns = [
    path('',include(router.urls))
]