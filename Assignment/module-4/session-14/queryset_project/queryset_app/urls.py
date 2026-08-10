from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'restaurants/',
        views.restaurant_filter,
        name='restaurant_filter'
    ),

    path(
        'products/',
        views.product_list,
        name='product_list'
    ),
]