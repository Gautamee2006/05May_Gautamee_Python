from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('orders/', views.my_orders, name='my_orders'),
    path('post-product/', views.post_product, name='post_product'),
    path('products/', views.product_list, name='product_list'),
    path('buy-product/<int:product_id>/', views.buy_product, name='buy_product'),
    path('movies/', views.movie_list, name='movie_list'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('reviews/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('playlist-admin/', views.playlist_admin_view, name='playlist_admin'),
]
