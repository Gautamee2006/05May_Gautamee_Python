from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('restaurants/', views.restaurant_list_view, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_detail_view, name='restaurant_detail'),
]
