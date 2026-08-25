from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Location, Cuisine, Restaurant, SearchHistory
from menu.models import MenuCategory, FoodItem
from offers.models import Offer
from reviews.models import Review
from favorites.models import Favorite

def home_view(request):
    cuisines = Cuisine.objects.all()[:8]
    locations = Location.objects.filter(is_active=True)
    top_restaurants = Restaurant.objects.filter(is_active=True).order_by('-rating')[:6]
    offers = Offer.objects.filter(is_active=True)[:4]

    # Selected location from query or default
    selected_location = request.GET.get('location', '')
    if selected_location:
        nearby_restaurants = Restaurant.objects.filter(is_active=True, location__name__iexact=selected_location)[:6]
    else:
        # Default to Rajkot or first location
        nearby_restaurants = Restaurant.objects.filter(is_active=True, location__name='Rajkot')[:6]
        if not nearby_restaurants.exists():
            nearby_restaurants = Restaurant.objects.filter(is_active=True)[:6]

    # Favorite IDs for logged-in user
    fav_ids = []
    if request.user.is_authenticated:
        fav_ids = list(Favorite.objects.filter(user=request.user).values_list('restaurant_id', flat=True))

    # Recently viewed restaurants
    recently_viewed_ids = request.session.get('recently_viewed', [])
    recently_viewed = Restaurant.objects.filter(id__in=recently_viewed_ids)[:4]

    context = {
        'cuisines': cuisines,
        'locations': locations,
        'top_restaurants': top_restaurants,
        'nearby_restaurants': nearby_restaurants,
        'selected_location': selected_location,
        'offers': offers,
        'fav_ids': fav_ids,
        'recently_viewed': recently_viewed,
    }
    return render(request, 'home.html', context)

def restaurant_list_view(request):
    restaurants = Restaurant.objects.filter(is_active=True)

    # 1. Search Query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        restaurants = restaurants.filter(
            Q(name__icontains=search_query) |
            Q(cuisine__name__icontains=search_query) |
            Q(location__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        if request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, query=search_query)

    # 2. Filters
    cuisine_filter = request.GET.get('cuisine', '').strip()
    if cuisine_filter:
        restaurants = restaurants.filter(cuisine__name__iexact=cuisine_filter)

    location_filter = request.GET.get('location', '').strip()
    if location_filter:
        restaurants = restaurants.filter(location__name__iexact=location_filter)

    min_rating = request.GET.get('rating', '').strip()
    if min_rating:
        try:
            restaurants = restaurants.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    price_filter = request.GET.get('price', '').strip()
    if price_filter:
        restaurants = restaurants.filter(price_range=price_filter)

    open_now = request.GET.get('open_now')
    if open_now == 'on':
        # Filter python objects in list
        restaurants_list = [r for r in restaurants if r.is_open_now()]
    else:
        restaurants_list = list(restaurants)

    # 3. Sorting
    sort_by = request.GET.get('sort_by', 'rating_desc')
    if sort_by == 'rating_desc':
        restaurants_list.sort(key=lambda r: r.rating, reverse=True)
    elif sort_by == 'rating_asc':
        restaurants_list.sort(key=lambda r: r.rating)
    elif sort_by == 'price_asc':
        price_order = {'$': 1, '$$': 2, '$$$': 3, '$$$$': 4}
        restaurants_list.sort(key=lambda r: price_order.get(r.price_range, 2))
    elif sort_by == 'price_desc':
        price_order = {'$': 1, '$$': 2, '$$$': 3, '$$$$': 4}
        restaurants_list.sort(key=lambda r: price_order.get(r.price_range, 2), reverse=True)
    elif sort_by == 'name_asc':
        restaurants_list.sort(key=lambda r: r.name.lower())

    # 4. Pagination
    paginator = Paginator(restaurants_list, 6) # 6 restaurants per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cuisines = Cuisine.objects.all()
    locations = Location.objects.filter(is_active=True)

    fav_ids = []
    if request.user.is_authenticated:
        fav_ids = list(Favorite.objects.filter(user=request.user).values_list('restaurant_id', flat=True))

    context = {
        'page_obj': page_obj,
        'cuisines': cuisines,
        'locations': locations,
        'search_query': search_query,
        'cuisine_filter': cuisine_filter,
        'location_filter': location_filter,
        'min_rating': min_rating,
        'price_filter': price_filter,
        'open_now': open_now,
        'sort_by': sort_by,
        'total_count': len(restaurants_list),
        'fav_ids': fav_ids,
    }
    return render(request, 'restaurants/restaurant_list.html', context)

def restaurant_detail_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)

    # Track recently viewed in session
    recently_viewed = request.session.get('recently_viewed', [])
    if restaurant.id in recently_viewed:
        recently_viewed.remove(restaurant.id)
    recently_viewed.insert(0, restaurant.id)
    request.session['recently_viewed'] = recently_viewed[:10]
    request.session.modified = True

    # Categories & Food Items
    categories = MenuCategory.objects.filter(restaurant=restaurant).prefetch_related('items')
    reviews = Review.objects.filter(restaurant=restaurant).select_related('user')
    offers = Offer.objects.filter(Q(restaurant=restaurant) | Q(restaurant__isnull=True), is_active=True)

    is_favorite = False
    user_review = None
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, restaurant=restaurant).exists()
        user_review = Review.objects.filter(user=request.user, restaurant=restaurant).first()

    context = {
        'restaurant': restaurant,
        'categories': categories,
        'reviews': reviews,
        'offers': offers,
        'is_favorite': is_favorite,
        'user_review': user_review,
    }
    return render(request, 'restaurants/restaurant_detail.html', context)
