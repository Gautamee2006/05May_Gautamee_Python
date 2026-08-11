from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('geocode/', views.geocode_view, name='geocode'),
    path('restaurant-location/', views.show_restaurant_location, name='restaurant_location'),
    path('search-distance/', views.search_by_distance, name='search_distance'),
]
