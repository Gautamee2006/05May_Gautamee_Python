from django.shortcuts import render

from django.db.models import Count, Q

from django.core.paginator import Paginator

from .models import (
    Restaurant,
    Movie,
    Product
)


# ==================================================
# HOME
# ==================================================

def home(request):

    return render(
        request,
        'queryset_app/home.html'
    )


# ==================================================
# TASK 1
# filter()
# ==================================================

def restaurant_filter(request):

    restaurants = Restaurant.objects.filter(

        cuisine='Chinese',

        rating__gt=4

    )


    return render(

        request,

        'queryset_app/home.html',

        {
            'restaurants':
                restaurants,

            'task':
                'Restaurant Filter'
        }
    )


# ==================================================
# TASK 3
# annotate()
# ==================================================

def movie_reviews(request):

    movies = Movie.objects.annotate(

        review_count=Count('reviews')

    )


    for movie in movies:

        print(
            movie.name,
            movie.review_count
        )


    return movies


# ==================================================
# TASK 4
# select_related()
# ==================================================

def product_with_category(request):

    products = Product.objects.select_related(
        'category'
    )


    for product in products:

        print(
            product.name,
            product.category.name
        )


    return products


# ==================================================
# TASK 5
# Q() + Paginator
# ==================================================

def product_list(request):

    products = Product.objects.filter(

        Q(
            category__name='Electronics'
        )

        |

        Q(
            price__lt=1000
        )

    )


    paginator = Paginator(
        products,
        5
    )


    page_number = request.GET.get(
        'page'
    )


    page_obj = paginator.get_page(
        page_number
    )


    return render(

        request,

        'queryset_app/home.html',

        {
            'products':
                page_obj,

            'page_obj':
                page_obj,

            'task':
                'Product Filter'
        }
    )