from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from restaurants.models import Restaurant
from menu.models import MenuCategory, FoodItem
from admin_panel.decorators import staff_required


@staff_required
def menu_list(request):
    restaurant_id = request.GET.get('restaurant', '')
    restaurants = Restaurant.objects.filter(is_active=True).order_by('name')
    selected_restaurant = None
    categories = []

    if restaurant_id:
        selected_restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        categories = MenuCategory.objects.filter(
            restaurant=selected_restaurant
        ).prefetch_related('items').order_by('order')
    else:
        # Show first restaurant by default
        selected_restaurant = restaurants.first()
        if selected_restaurant:
            categories = MenuCategory.objects.filter(
                restaurant=selected_restaurant
            ).prefetch_related('items').order_by('order')

    context = {
        'restaurants': restaurants,
        'selected_restaurant': selected_restaurant,
        'categories': categories,
        'page_title': 'Menu Management',
        'active_nav': 'menu',
    }
    return render(request, 'admin_panel/menu/list.html', context)


@staff_required
def category_add(request):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=request.POST.get('restaurant'))
        name = request.POST.get('name', '').strip()
        order = request.POST.get('order', 1)
        if name:
            MenuCategory.objects.create(restaurant=restaurant, name=name, order=order)
            messages.success(request, f"Category '{name}' added to {restaurant.name}.")
        return redirect(f'/panel/menu/?restaurant={restaurant.id}')
    return redirect('panel_menu_list')


@staff_required
def category_delete(request, pk):
    cat = get_object_or_404(MenuCategory, pk=pk)
    restaurant_id = cat.restaurant.id
    if request.method == 'POST':
        name = cat.name
        cat.delete()
        messages.success(request, f"Category '{name}' deleted.")
    return redirect(f'/panel/menu/?restaurant={restaurant_id}')


@staff_required
def food_item_add(request):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=request.POST.get('restaurant'))
        category = get_object_or_404(MenuCategory, id=request.POST.get('category'))
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price', 0)
        description = request.POST.get('description', '')
        image = request.POST.get('image', '')
        is_vegetarian = request.POST.get('is_vegetarian') == 'on'
        is_available = request.POST.get('is_available') == 'on'

        if name and price:
            FoodItem.objects.create(
                restaurant=restaurant,
                category=category,
                name=name,
                price=price,
                description=description,
                image=image,
                is_vegetarian=is_vegetarian,
                is_available=is_available,
            )
            messages.success(request, f"Food item '{name}' added successfully!")
        return redirect(f'/panel/menu/?restaurant={restaurant.id}')
    return redirect('panel_menu_list')


@staff_required
def food_item_edit(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    restaurant_id = item.restaurant.id

    if request.method == 'POST':
        item.name = request.POST.get('name', item.name).strip()
        item.price = request.POST.get('price', item.price)
        item.description = request.POST.get('description', item.description)
        item.image = request.POST.get('image', item.image)
        item.is_vegetarian = request.POST.get('is_vegetarian') == 'on'
        item.is_available = request.POST.get('is_available') == 'on'
        cat_id = request.POST.get('category')
        if cat_id:
            item.category = get_object_or_404(MenuCategory, id=cat_id)
        item.save()
        messages.success(request, f"Food item '{item.name}' updated!")
        return redirect(f'/panel/menu/?restaurant={restaurant_id}')

    categories = MenuCategory.objects.filter(restaurant=item.restaurant)
    return render(request, 'admin_panel/menu/item_form.html', {
        'item': item,
        'categories': categories,
        'page_title': f'Edit: {item.name}',
        'active_nav': 'menu',
    })


@staff_required
def food_item_delete(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    restaurant_id = item.restaurant.id
    if request.method == 'POST':
        name = item.name
        item.delete()
        messages.success(request, f"Food item '{name}' deleted.")
    return redirect(f'/panel/menu/?restaurant={restaurant_id}')


@staff_required
def food_item_toggle(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    restaurant_id = item.restaurant.id
    if request.method == 'POST':
        item.is_available = not item.is_available
        item.save()
        status = 'available' if item.is_available else 'unavailable'
        messages.success(request, f"'{item.name}' marked as {status}.")
    return redirect(f'/panel/menu/?restaurant={restaurant_id}')
