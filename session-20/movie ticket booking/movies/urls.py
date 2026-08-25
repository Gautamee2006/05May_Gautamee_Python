from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list_view, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail_view, name='movie_detail'),
    path('shows/<int:show_id>/seats/', views.seat_selection_view, name='seat_selection'),
    path('shows/<int:show_id>/book/', views.book_ticket_view, name='book_ticket'),
    path('booking/<str:booking_id>/confirmation/', views.booking_confirmation_view, name='booking_confirmation'),
    path('booking/<str:booking_id>/detail/', views.booking_detail_view, name='booking_detail'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
]
