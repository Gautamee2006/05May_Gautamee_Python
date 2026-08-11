import os
import math
import requests
from django.conf import settings


class GeocodeResult(tuple):
    """
    A tuple subclass (lat, lng) that also carries an error attribute.
    Supports tuple unpacking: lat, lng = geocode_address(...)
    """
    def __new__(cls, lat, lng, error=None):
        instance = super().__new__(cls, (lat, lng))
        instance.lat = lat
        instance.lng = lng
        instance.error = error
        return instance


def geocode_address(address):
    """
    Geocodes an address string using Google Geocoding API.
    
    Returns a GeocodeResult (lat, lng) tuple.
    Unpacking: lat, lng = geocode_address("IIM Ahmedabad, Gujarat")
    Error check: result = geocode_address(...); if result.error: ...
    """
    if not address or not isinstance(address, str) or not address.strip():
        return GeocodeResult(None, None, error="Address cannot be empty.")

    api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '') or os.getenv('GOOGLE_MAPS_API_KEY', '')
    if not api_key or api_key == 'your_google_maps_api_key_here':
        return GeocodeResult(
            None, None,
            error="Google Maps API Key is missing or not configured in .env file."
        )

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address.strip(),
        'key': api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
    except requests.exceptions.RequestException as e:
        return GeocodeResult(
            None, None,
            error=f"Network error connecting to Google Geocoding API: {str(e)}"
        )
    except Exception as e:
        return GeocodeResult(
            None, None,
            error=f"Unexpected error while geocoding: {str(e)}"
        )

    status = data.get('status')
    if status == 'OK' and data.get('results'):
        location = data['results'][0]['geometry']['location']
        lat = float(location['lat'])
        lng = float(location['lng'])
        return GeocodeResult(lat, lng, error=None)
    elif status == 'ZERO_RESULTS':
        return GeocodeResult(
            None, None,
            error=f"No location results found for '{address}'. Please try a different address."
        )
    elif status == 'REQUEST_DENIED':
        return GeocodeResult(
            None, None,
            error="Google API Key request was denied. Please verify your key and ensure Geocoding API is enabled."
        )
    elif status == 'OVER_QUERY_LIMIT':
        return GeocodeResult(
            None, None,
            error="Google Maps API quota exceeded."
        )
    else:
        error_msg = data.get('error_message', f"Geocoding API error (Status: {status}).")
        return GeocodeResult(None, None, error=error_msg)


def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates manual Haversine distance in kilometers between two lat/lng points.
    Uses ONLY Python's built-in math module.
    
    Formula:
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)^2 + cos(lat1) * cos(lat2) * sin(dlon/2)^2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    """
    R = 6371.0  # Earth's radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    rad_lat1 = math.radians(lat1)
    rad_lat2 = math.radians(lat2)

    a = (math.sin(dlat / 2.0) ** 2) + math.cos(rad_lat1) * math.cos(rad_lat2) * (math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    distance = R * c
    return distance


def find_nearby_cafes(user_lat, user_lng, cafes):
    """
    Task 3 requirement: Accepts user_lat, user_lng, and a list of cafe dicts:
    [{"name": "Cafe A", "lat": 23.0225, "lng": 72.5714}, ...]
    
    Calculates distance manually using Haversine formula and returns cafes within 3 km.
    Includes calculated distance in the returned result.
    """
    nearby_cafes = []
    if user_lat is None or user_lng is None or not cafes:
        return nearby_cafes

    try:
        u_lat = float(user_lat)
        u_lng = float(user_lng)
    except (ValueError, TypeError):
        return nearby_cafes

    for cafe in cafes:
        c_lat = cafe.get('lat')
        c_lng = cafe.get('lng')
        if c_lat is not None and c_lng is not None:
            dist = calculate_haversine_distance(u_lat, u_lng, float(c_lat), float(c_lng))
            if dist <= 3.0:
                cafe_info = cafe.copy()
                cafe_info['distance'] = round(dist, 2)
                nearby_cafes.append(cafe_info)

    nearby_cafes.sort(key=lambda item: item['distance'])
    return nearby_cafes
