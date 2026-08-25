from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<str:order_id>/', views.order_success_view, name='order_success'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('detail/<str:order_id>/', views.order_detail_view, name='order_detail'),
    path('cancel/<str:order_id>/', views.cancel_order_view, name='cancel_order'),
    path('return/<str:order_id>/', views.return_product_view, name='return_product'),
    path('invoice/<str:order_id>/', views.invoice_view, name='invoice'),
]
