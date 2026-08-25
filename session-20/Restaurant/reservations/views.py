from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, date
from restaurants.models import Restaurant
from .models import Reservation

@login_required
def create_reservation_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)

    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        num_people = request.POST.get('num_people', 2)
        special_request = request.POST.get('special_request', '').strip()

        try:
            res_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if res_date < date.today():
                messages.error(request, "Reservation date cannot be in the past.")
                return redirect('restaurant_detail', restaurant_id=restaurant.id)

            res_time = datetime.strptime(time_str, '%H:%M').time()
            guests = int(num_people)

            if guests < 1 or guests > 20:
                messages.error(request, "Please enter a valid guest count (1-20).")
                return redirect('restaurant_detail', restaurant_id=restaurant.id)

            reservation = Reservation.objects.create(
                user=request.user,
                restaurant=restaurant,
                date=res_date,
                time=res_time,
                num_people=guests,
                special_request=special_request,
                status='pending'
            )

            messages.success(request, f"Table reservation submitted for {restaurant.name}! Booking ID: #{reservation.id}")
            return redirect('reservation_list')

        except (ValueError, TypeError) as e:
            messages.error(request, "Invalid date or time format.")
            return redirect('restaurant_detail', restaurant_id=restaurant.id)

    return redirect('restaurant_detail', restaurant_id=restaurant_id)

@login_required
def reservation_list_view(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('restaurant')
    return render(request, 'reservations/reservation_list.html', {'reservations': reservations})

@login_required
def cancel_reservation_view(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
        if reservation.status in ['pending', 'confirmed']:
            reservation.status = 'cancelled'
            reservation.save()
            messages.info(request, f"Reservation #{reservation.id} has been cancelled.")
        else:
            messages.warning(request, "This reservation cannot be cancelled.")
    return redirect('reservation_list')
