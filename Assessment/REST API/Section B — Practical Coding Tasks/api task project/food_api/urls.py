from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListView,
    MenuItemListCreateView,
    MenuItemDetailView,
    OrderViewSet,
    PlaceOrderAPIView,
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('menu-items/', MenuItemListCreateView.as_view(), name='menuitem-list-create'),
    path('menu-items/<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
    path('my-orders/', PlaceOrderAPIView.as_view(), name='my-orders'),
    path('', include(router.urls)),
]
