from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('gateway/<str:order_id>/', views.payment_gateway_view, name='payment_gateway'),
]
