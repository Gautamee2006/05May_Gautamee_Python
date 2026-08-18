from django.urls import path, include
from rest_framework.routers import DefaultRouter
from food_api.views import CategoryViewSet, MenuItemViewSet, OrderViewSet, my_orders

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('menu-items', MenuItemViewSet, basename='menuitem')
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('my-orders/', my_orders, name='my-orders'),
]
