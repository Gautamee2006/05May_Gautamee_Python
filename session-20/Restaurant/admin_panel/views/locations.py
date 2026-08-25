from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from restaurants.models import Location, Cuisine
from admin_panel.decorators import staff_required


@staff_required
def location_list(request):
    locations = Location.objects.all().order_by('name')
    return render(request, 'admin_panel/locations/list.html', {
        'locations': locations,
        'page_title': 'Locations & Cuisines',
        'active_nav': 'locations',
    })


@staff_required
def location_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        state = request.POST.get('state', '').strip()
        if name:
            obj, created = Location.objects.get_or_create(name=name, defaults={'state': state})
            if created:
                messages.success(request, f"Location '{name}' added!")
            else:
                messages.warning(request, f"Location '{name}' already exists.")
    return redirect('panel_location_list')


@staff_required
def location_delete(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        name = location.name
        location.delete()
        messages.success(request, f"Location '{name}' deleted.")
    return redirect('panel_location_list')


@staff_required
def cuisine_list(request):
    cuisines = Cuisine.objects.all().order_by('name')
    return render(request, 'admin_panel/locations/list.html', {
        'cuisines': cuisines,
        'locations': Location.objects.all().order_by('name'),
        'page_title': 'Locations & Cuisines',
        'active_nav': 'locations',
    })


@staff_required
def cuisine_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        icon = request.POST.get('icon', 'fa-utensils').strip()
        if name:
            obj, created = Cuisine.objects.get_or_create(name=name, defaults={'icon': icon})
            if created:
                messages.success(request, f"Cuisine '{name}' added!")
            else:
                messages.warning(request, f"Cuisine '{name}' already exists.")
    return redirect('panel_location_list')


@staff_required
def cuisine_delete(request, pk):
    cuisine = get_object_or_404(Cuisine, pk=pk)
    if request.method == 'POST':
        name = cuisine.name
        cuisine.delete()
        messages.success(request, f"Cuisine '{name}' deleted.")
    return redirect('panel_location_list')
