from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/<int:restaurant_id>/review/', views.add_review_view, name='add_review'),
]
