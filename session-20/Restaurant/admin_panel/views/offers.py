from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from offers.models import Offer
from restaurants.models import Restaurant
from admin_panel.decorators import staff_required
from datetime import date


@staff_required
def offer_list(request):
    status_filter = request.GET.get('status', '')
    restaurant_filter = request.GET.get('restaurant', '')

    offers = Offer.objects.select_related('restaurant').order_by('-end_date')

    if status_filter == 'active':
        offers = offers.filter(is_active=True, end_date__gte=date.today())
    elif status_filter == 'inactive':
        offers = offers.filter(is_active=False)
    elif status_filter == 'expired':
        offers = offers.filter(end_date__lt=date.today())
    if restaurant_filter:
        offers = offers.filter(restaurant_id=restaurant_filter)

    context = {
        'offers': offers,
        'restaurants': Restaurant.objects.filter(is_active=True),
        'status_filter': status_filter,
        'restaurant_filter': restaurant_filter,
        'today': date.today(),
        'page_title': 'Offers & Coupons',
        'active_nav': 'offers',
    }
    return render(request, 'admin_panel/offers/list.html', context)


@staff_required
def offer_add(request):
    restaurants = Restaurant.objects.filter(is_active=True)
    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant')
        restaurant = Restaurant.objects.filter(id=restaurant_id).first() if restaurant_id else None

        offer = Offer.objects.create(
            restaurant=restaurant,
            title=request.POST.get('title', '').strip(),
            description=request.POST.get('description', ''),
            discount_percentage=request.POST.get('discount_percentage', 0),
            coupon_code=request.POST.get('coupon_code', '').strip().upper(),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, f"Offer '{offer.title}' (Code: {offer.coupon_code}) created!")
        return redirect('panel_offer_list')

    return render(request, 'admin_panel/offers/form.html', {
        'restaurants': restaurants,
        'page_title': 'Add Offer',
        'active_nav': 'offers',
    })


@staff_required
def offer_edit(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    restaurants = Restaurant.objects.filter(is_active=True)

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant')
        offer.restaurant = Restaurant.objects.filter(id=restaurant_id).first() if restaurant_id else None
        offer.title = request.POST.get('title', offer.title).strip()
        offer.description = request.POST.get('description', offer.description)
        offer.discount_percentage = request.POST.get('discount_percentage', offer.discount_percentage)
        offer.coupon_code = request.POST.get('coupon_code', offer.coupon_code).strip().upper()
        offer.start_date = request.POST.get('start_date', offer.start_date)
        offer.end_date = request.POST.get('end_date', offer.end_date)
        offer.is_active = request.POST.get('is_active') == 'on'
        offer.save()
        messages.success(request, f"Offer '{offer.title}' updated!")
        return redirect('panel_offer_list')

    return render(request, 'admin_panel/offers/form.html', {
        'offer': offer,
        'restaurants': restaurants,
        'page_title': f'Edit Offer: {offer.title}',
        'active_nav': 'offers',
    })


@staff_required
def offer_delete(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        title = offer.title
        offer.delete()
        messages.success(request, f"Offer '{title}' deleted.")
    return redirect('panel_offer_list')


@staff_required
def offer_toggle(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.method == 'POST':
        offer.is_active = not offer.is_active
        offer.save()
        status = 'activated' if offer.is_active else 'deactivated'
        messages.success(request, f"Offer '{offer.title}' {status}.")
    return redirect('panel_offer_list')
