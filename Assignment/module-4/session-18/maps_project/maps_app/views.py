import os
from django.shortcuts import render
from django.conf import settings
from .utils import geocode_address, calculate_haversine_distance, find_nearby_cafes

# Task 4 Hardcoded Pickup Point Addresses (At least 5 addresses required)
HARDCODED_PICKUP_POINTS = [
    {
        "name": "Flipkart Pickup Hub - Navrangpura",
        "address": "Navrangpura, Ahmedabad, Gujarat",
        "fallback_lat": 23.0365,
        "fallback_lng": 72.5611,
    },
    {
        "name": "Flipkart Pickup Hub - Satellite",
        "address": "Satellite, Ahmedabad, Gujarat",
        "fallback_lat": 23.0300,
        "fallback_lng": 72.5178,
    },
    {
        "name": "Flipkart Pickup Hub - SG Highway",
        "address": "SG Highway, Ahmedabad, Gujarat",
        "fallback_lat": 23.0524,
        "fallback_lng": 72.5028,
    },
    {
        "name": "Flipkart Pickup Hub - Maninagar",
        "address": "Maninagar, Ahmedabad, Gujarat",
        "fallback_lat": 22.9978,
        "fallback_lng": 72.6030,
    },
    {
        "name": "Flipkart Pickup Hub - Vastrapur",
        "address": "Vastrapur, Ahmedabad, Gujarat",
        "fallback_lat": 23.0350,
        "fallback_lng": 72.5293,
    },
]


def home(request):
    """
    Home View: Displays links to Task 1, Task 2, and Task 4 features.
    """
    return render(request, 'maps_app/home.html')


def geocode_view(request):
    """
    Task 1 View: Address Geocoding page.
    Receives user input address, requests Google Geocoding API, and displays coordinates.
    """
    context = {}
    if request.method == 'POST' or request.GET.get('address'):
        address = request.POST.get('address') or request.GET.get('address')
        context['address'] = address
        
        result = geocode_address(address)
        if result.error:
            context['error'] = result.error
        else:
            context['latitude'] = result.lat
            context['longitude'] = result.lng
            
    return render(request, 'maps_app/geocode.html', context)


def show_restaurant_location(request):
    """
    Task 2 View: Displays restaurant address, lat/lng, and Google Map Embed.
    """
    context = {
        'google_api_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', '') or os.getenv('GOOGLE_MAPS_API_KEY', '')
    }
    
    if request.method == 'POST' or request.GET.get('address'):
        address = request.POST.get('address') or request.GET.get('address')
        context['address'] = address

        result = geocode_address(address)
        if result.error:
            context['error'] = result.error
        else:
            context['latitude'] = result.lat
            context['longitude'] = result.lng

    return render(request, 'maps_app/restaurant_location.html', context)


def search_by_distance(request):
    """
    Task 4 View: Pickup Point Distance Search.
    Receives current user address dynamically, geocodes it, geocodes 5 pickup points,
    calculates manual Haversine distance, and displays results sorted nearest -> farthest.
    """
    context = {}
    
    if request.method == 'POST' or request.GET.get('address'):
        user_address = request.POST.get('address') or request.GET.get('address')
        context['user_address'] = user_address

        # Geocode user address
        user_result = geocode_address(user_address)
        
        if user_result.error and not (user_result.lat and user_result.lng):
            context['error'] = user_result.error
        else:
            user_lat = user_result.lat
            user_lng = user_result.lng
            context['user_latitude'] = user_lat
            context['user_longitude'] = user_lng

            # Process 5 hardcoded pickup points
            processed_points = []
            for item in HARDCODED_PICKUP_POINTS:
                point_lat, point_lng = None, None
                
                # Attempt to geocode hardcoded pickup point address dynamically
                geocode_res = geocode_address(item['address'])
                if geocode_res.lat is not None and geocode_res.lng is not None:
                    point_lat = geocode_res.lat
                    point_lng = geocode_res.lng
                else:
                    # Fallback to predefined coordinates if API key is unconfigured or rate limited
                    point_lat = item['fallback_lat']
                    point_lng = item['fallback_lng']

                # Calculate distance using manual Haversine formula
                dist = calculate_haversine_distance(user_lat, user_lng, point_lat, point_lng)
                
                processed_points.append({
                    'name': item['name'],
                    'address': item['address'],
                    'latitude': point_lat,
                    'longitude': point_lng,
                    'distance': round(dist, 2)
                })

            # Sort pickup points ascending: nearest -> farthest
            processed_points.sort(key=lambda x: x['distance'])
            context['pickup_points'] = processed_points

    return render(request, 'maps_app/distance_search.html', context)
