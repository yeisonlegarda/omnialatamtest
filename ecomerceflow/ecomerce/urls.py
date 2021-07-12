from ecomerce.views import ProductsViewSet, OrderViewSet
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('products',ProductsViewSet)
router.register('orders',OrderViewSet)

app_name = 'product'

urlpatterns = [
    path('',include(router.urls))
]