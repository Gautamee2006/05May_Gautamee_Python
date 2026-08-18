from django.urls import path
from .views import PlaceOrderAPIView

urlpatterns = [
    path('place/', PlaceOrderAPIView.as_view(), name='place-order'),
]
