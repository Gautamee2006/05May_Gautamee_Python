from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home_view, name='home'),
    path('products/', views.dashboard_products_view, name='products'),
    path('products/edit/<int:product_id>/', views.dashboard_edit_product_view, name='edit_product'),
    path('products/delete/<int:product_id>/', views.dashboard_delete_product_view, name='delete_product'),
    path('orders/', views.dashboard_orders_view, name='orders'),
    path('users/', views.dashboard_users_view, name='users'),
    path('inventory/', views.dashboard_inventory_view, name='inventory'),
    path('coupons/', views.dashboard_coupons_view, name='coupons'),
    path('coupons/delete/<int:coupon_id>/', views.dashboard_delete_coupon_view, name='delete_coupon'),
    path('tickets/', views.dashboard_tickets_view, name='tickets'),
]
