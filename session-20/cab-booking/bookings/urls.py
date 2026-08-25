from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('book/', views.book_cab_view, name='book_cab'),
    path('confirmation/<str:booking_id>/', views.booking_confirmation_view, name='booking_confirmation'),
    path('bookings/', views.booking_history_view, name='booking_history'),
    
    # API endpoints
    path('api/bookings/create/', views.api_create_booking, name='api_create_booking'),
    path('api/bookings/<str:booking_id>/cancel/', views.api_cancel_booking, name='api_cancel_booking'),
    
    # Auth routes
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
