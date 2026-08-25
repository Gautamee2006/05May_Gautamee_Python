from django.urls import path
from . import views

urlpatterns = [
    path('favorites/', views.favorites_list_view, name='favorites_list'),
    path('favorites/toggle/<int:restaurant_id>/', views.toggle_favorite_view, name='toggle_favorite'),
]
