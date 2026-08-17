from django.urls import path
from . import views

urlpatterns = [
    path('music-weather/<str:city>/', views.music_weather, name='music_weather'),
    path('food-location/', views.food_location, name='food_location'),
    path('country-info/<str:country_name>/', views.country_info, name='country_info'),
    path('github-repos/<str:username>/', views.github_repos, name='github_repos'),
]
