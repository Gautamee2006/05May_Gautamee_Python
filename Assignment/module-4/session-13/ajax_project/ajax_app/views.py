import json

from django.shortcuts import render

from django.http import JsonResponse

from .models import Song, Product, Movie, Playlist


# ==================================================
# HOME
# ==================================================

def home(request):

    return render(
        request,
        'ajax_app/home.html'
    )


# ==================================================
# TASK 1 - SONGS
# ==================================================

def songs(request):

    songs = Song.objects.all()

    return render(
        request,
        'ajax_app/songs.html',
        {
            'songs': songs
        }
    )


def delete_song(request, id):

    if request.method == 'DELETE':

        try:

            song = Song.objects.get(id=id)

            song.delete()

            return JsonResponse({

                'success': True,

                'message': 'Song deleted successfully.'

            })

        except Song.DoesNotExist:

            return JsonResponse({

                'success': False,

                'message': 'Song not found.'

            }, status=404)


    return JsonResponse({

        'success': False,

        'message': 'Invalid request.'

    }, status=400)


# ==================================================
# TASK 2 - PRODUCTS
# ==================================================

def products(request):

    products = Product.objects.all()

    return render(
        request,
        'ajax_app/products.html',
        {
            'products': products
        }
    )


def delete_product(request, id):

    if request.method == 'DELETE':

        try:

            product = Product.objects.get(id=id)

            product.delete()

            return JsonResponse({

                'success': True,

                'message': 'Product removed from wishlist.'

            })

        except Product.DoesNotExist:

            return JsonResponse({

                'success': False,

                'message': 'Product not found.'

            }, status=404)


    return JsonResponse({

        'success': False,

        'message': 'Invalid request.'

    }, status=400)


# ==================================================
# TASK 3 - MOVIES
# ==================================================

def movies(request):

    movies = Movie.objects.all()

    return render(
        request,
        'ajax_app/movies.html',
        {
            'movies': movies
        }
    )


def delete_movie(request, id):

    if request.method == 'DELETE':

        try:

            # JSON request read karva
            data = json.loads(
                request.body
            )

            movie_id = data.get(
                'movie_id'
            )

            # ID URL mathi levu
            movie = Movie.objects.get(
                id=movie_id
            )

            movie_name = movie.name

            movie.delete()

            return JsonResponse({

                'success': True,

                'message':
                    f'"{movie_name}" removed from Watch Later.'

            })

        except Movie.DoesNotExist:

            return JsonResponse({

                'success': False,

                'message': 'Movie not found.'

            }, status=404)

        except json.JSONDecodeError:

            return JsonResponse({

                'success': False,

                'message': 'Invalid JSON.'

            }, status=400)


    return JsonResponse({

        'success': False,

        'message': 'Invalid request.'

    }, status=400)


# ==================================================
# TASK 4 - PLAYLIST
# ==================================================

def playlists(request):

    playlists = Playlist.objects.all()

    return render(
        request,
        'ajax_app/playlists.html',
        {
            'playlists': playlists
        }
    )


def delete_playlist(request, id):

    if request.method == 'DELETE':

        try:

            playlist = Playlist.objects.get(
                id=id
            )

            playlist.delete()

            return JsonResponse({

                'success': True,

                'message':
                    'Playlist deleted successfully.'

            })

        except Playlist.DoesNotExist:

            return JsonResponse({

                'success': False,

                'message': 'Playlist not found.'

            }, status=404)


    return JsonResponse({

        'success': False,

        'message': 'Invalid request.'

    }, status=400)