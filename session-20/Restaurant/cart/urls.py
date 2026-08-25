from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_detail_view, name='cart_detail'),
    path('cart/add/<int:food_item_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item_view, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item_view, name='remove_cart_item'),
    path('cart/clear/', views.clear_cart_view, name='clear_cart'),
    path('cart/apply-coupon/', views.apply_coupon_view, name='apply_coupon'),
]
