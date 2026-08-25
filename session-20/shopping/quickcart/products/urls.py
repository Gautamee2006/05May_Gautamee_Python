from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='product_list'),
    path('search/', views.search_view, name='search'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('detail/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('review/add/<int:product_id>/', views.add_review_view, name='add_review'),
]
