from django.urls import path
from . import views

urlpatterns = [
    path('reservations/', views.reservation_list_view, name='reservation_list'),
    path('restaurants/<int:restaurant_id>/reserve/', views.create_reservation_view, name='create_reservation'),
    path('reservations/cancel/<int:reservation_id>/', views.cancel_reservation_view, name='cancel_reservation'),
]
