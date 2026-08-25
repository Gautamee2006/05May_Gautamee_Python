from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('orders/', views.order_list_view, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('orders/<int:order_id>/confirmation/', views.order_confirmation_view, name='order_confirmation'),
    path('orders/<int:order_id>/cancel/', views.cancel_order_view, name='cancel_order'),
]
