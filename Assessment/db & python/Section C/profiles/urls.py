from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_list, name='profile_list'),
    path('create/', views.profile_create, name='profile_create'),
    path('edit/<int:id>/', views.profile_edit, name='profile_edit'),
    path('export/', views.profile_export, name='profile_export'),
]
