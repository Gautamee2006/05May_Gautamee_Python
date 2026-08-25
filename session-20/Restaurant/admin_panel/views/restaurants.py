from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from restaurants.models import Restaurant, Cuisine, Location
from admin_panel.decorators import staff_required


@staff_required
def restaurant_list(request):
    search = request.GET.get('search', '')
    cuisine_filter = request.GET.get('cuisine', '')
    location_filter = request.GET.get('location', '')
    status_filter = request.GET.get('status', '')

    restaurants = Restaurant.objects.select_related('cuisine', 'location').all()

    if search:
        restaurants = restaurants.filter(name__icontains=search)
    if cuisine_filter:
        restaurants = restaurants.filter(cuisine__name=cuisine_filter)
    if location_filter:
        restaurants = restaurants.filter(location__name=location_filter)
    if status_filter == 'active':
        restaurants = restaurants.filter(is_active=True)
    elif status_filter == 'inactive':
        restaurants = restaurants.filter(is_active=False)

    context = {
        'restaurants': restaurants,
        'cuisines': Cuisine.objects.all(),
        'locations': Location.objects.all(),
        'search': search,
        'cuisine_filter': cuisine_filter,
        'location_filter': location_filter,
        'status_filter': status_filter,
        'page_title': 'Restaurant Management',
        'active_nav': 'restaurants',
    }
    return render(request, 'admin_panel/restaurants/list.html', context)


@staff_required
def restaurant_add(request):
    cuisines = Cuisine.objects.all()
    locations = Location.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if not name:
            messages.error(request, 'Restaurant name is required.')
            return render(request, 'admin_panel/restaurants/form.html', {
                'cuisines': cuisines, 'locations': locations,
                'page_title': 'Add Restaurant', 'active_nav': 'restaurants',
            })

        cuisine = get_object_or_404(Cuisine, id=request.POST.get('cuisine'))
        location = get_object_or_404(Location, id=request.POST.get('location'))

        restaurant = Restaurant.objects.create(
            name=name,
            cuisine=cuisine,
            location=location,
            address=request.POST.get('address', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            description=request.POST.get('description', ''),
            price_range=request.POST.get('price_range', '$$'),
            opening_time=request.POST.get('opening_time', '09:00'),
            closing_time=request.POST.get('closing_time', '23:00'),
            image=request.POST.get('image', ''),
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, f"Restaurant '{restaurant.name}' added successfully!")
        return redirect('panel_restaurant_list')

    return render(request, 'admin_panel/restaurants/form.html', {
        'cuisines': cuisines, 'locations': locations,
        'page_title': 'Add Restaurant', 'active_nav': 'restaurants',
    })


@staff_required
def restaurant_edit(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    cuisines = Cuisine.objects.all()
    locations = Location.objects.all()

    if request.method == 'POST':
        restaurant.name = request.POST.get('name', restaurant.name).strip()
        restaurant.cuisine = get_object_or_404(Cuisine, id=request.POST.get('cuisine'))
        restaurant.location = get_object_or_404(Location, id=request.POST.get('location'))
        restaurant.address = request.POST.get('address', '')
        restaurant.phone = request.POST.get('phone', '')
        restaurant.email = request.POST.get('email', '')
        restaurant.description = request.POST.get('description', '')
        restaurant.price_range = request.POST.get('price_range', '$$')
        restaurant.opening_time = request.POST.get('opening_time', '09:00')
        restaurant.closing_time = request.POST.get('closing_time', '23:00')
        restaurant.image = request.POST.get('image', restaurant.image)
        restaurant.is_active = request.POST.get('is_active') == 'on'
        restaurant.save()
        messages.success(request, f"Restaurant '{restaurant.name}' updated!")
        return redirect('panel_restaurant_list')

    return render(request, 'admin_panel/restaurants/form.html', {
        'restaurant': restaurant, 'cuisines': cuisines, 'locations': locations,
        'page_title': f'Edit: {restaurant.name}', 'active_nav': 'restaurants',
    })


@staff_required
def restaurant_delete(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        name = restaurant.name
        restaurant.delete()
        messages.success(request, f"Restaurant '{name}' deleted.")
    return redirect('panel_restaurant_list')


@staff_required
def restaurant_toggle(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.is_active = not restaurant.is_active
        restaurant.save()
        status = 'activated' if restaurant.is_active else 'deactivated'
        messages.success(request, f"Restaurant '{restaurant.name}' {status}.")
    return redirect('panel_restaurant_list')
