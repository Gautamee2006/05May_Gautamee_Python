from django.urls import path
from .views import PlaylistView, OrderView, CartView, TicketView

urlpatterns = [
    path('playlists/', PlaylistView.as_view(), name='playlist-list'),
    path('orders/', OrderView.as_view(), name='order-list'),
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('tickets/', TicketView.as_view(), name='ticket-list'),
]
