from django.urls import path

from . import views


urlpatterns = [

    # Home
    path(
        '',
        views.home,
        name='home'
    ),


    # --------------------------------
    # SONGS
    # --------------------------------

    path(
        'songs/',
        views.songs,
        name='songs'
    ),

    path(
        'songs/<int:id>/delete/',
        views.delete_song,
        name='delete_song'
    ),


    # --------------------------------
    # PRODUCTS
    # --------------------------------

    path(
        'products/',
        views.products,
        name='products'
    ),

    path(
        'products/<int:id>/delete/',
        views.delete_product,
        name='delete_product'
    ),


    # --------------------------------
    # MOVIES
    # --------------------------------

    path(
        'movies/',
        views.movies,
        name='movies'
    ),

    path(
        'movies/<int:id>/delete/',
        views.delete_movie,
        name='delete_movie'
    ),


    # --------------------------------
    # PLAYLISTS
    # --------------------------------

    path(
        'playlists/',
        views.playlists,
        name='playlists'
    ),

    path(
        'playlists/<int:id>/delete/',
        views.delete_playlist,
        name='delete_playlist'
    ),
]