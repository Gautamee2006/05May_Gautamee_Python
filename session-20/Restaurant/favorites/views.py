from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from restaurants.models import Restaurant
from .models import Favorite

@login_required
def toggle_favorite_view(request, restaurant_id):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
        if created:
            messages.success(request, f"Added {restaurant.name} to your favorites! ❤️")
        else:
            favorite.delete()
            messages.info(request, f"Removed {restaurant.name} from your favorites.")
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else 'favorites_list')

@login_required
def favorites_list_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('restaurant', 'restaurant__cuisine', 'restaurant__location')
    return render(request, 'favorites/favorite_list.html', {'favorites': favorites})
