from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from reservations.models import Reservation
from restaurants.models import Restaurant
from admin_panel.decorators import staff_required


@staff_required
def reservation_list(request):
    status_filter = request.GET.get('status', '')
    restaurant_filter = request.GET.get('restaurant', '')
    date_filter = request.GET.get('date', '')
    search = request.GET.get('search', '')

    reservations = Reservation.objects.select_related('user', 'restaurant').order_by('-created_at')

    if status_filter:
        reservations = reservations.filter(status=status_filter)
    if restaurant_filter:
        reservations = reservations.filter(restaurant_id=restaurant_filter)
    if date_filter:
        reservations = reservations.filter(date=date_filter)
    if search:
        reservations = reservations.filter(user__username__icontains=search)

    context = {
        'reservations': reservations[:100],
        'restaurants': Restaurant.objects.filter(is_active=True),
        'status_filter': status_filter,
        'restaurant_filter': restaurant_filter,
        'date_filter': date_filter,
        'search': search,
        'status_choices': Reservation.STATUS_CHOICES,
        'page_title': 'Reservation Management',
        'active_nav': 'reservations',
    }
    return render(request, 'admin_panel/reservations/list.html', context)


@staff_required
def reservation_update_status(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Reservation.STATUS_CHOICES):
            reservation.status = new_status
            reservation.save()
            messages.success(request, f"Reservation #{reservation.id} status updated to '{new_status}'.")
        else:
            messages.error(request, "Invalid status.")
    return redirect('panel_reservation_list')
