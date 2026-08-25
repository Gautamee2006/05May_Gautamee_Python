import json
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Booking
from .forms import RegisterForm

DRIVER_POOL = [
    {"name": "Rahul Patel", "vehicle": "Swift Dzire", "number": "GJ03AB1234", "phone": "+91 98765 43210", "rating": 4.9},
    {"name": "Vikram Singh", "vehicle": "Hyundai Aura", "number": "GJ01CD5678", "phone": "+91 98765 11223", "rating": 4.8},
    {"name": "Amit Shah", "vehicle": "Toyota Innova", "number": "GJ05EF9012", "phone": "+91 98765 44332", "rating": 4.95},
    {"name": "Sanjay Mehta", "vehicle": "Ertiga", "number": "GJ03GH3456", "phone": "+91 98765 99887", "rating": 4.7},
]

def home_view(request):
    """Landing Home Page"""
    recent_bookings = []
    if request.user.is_authenticated:
        recent_bookings = Booking.objects.filter(user=request.user)[:3]
    return render(request, 'bookings/home.html', {
        'recent_bookings': recent_bookings
    })

@login_required
def book_cab_view(request):
    """Main interactive map & cab booking dashboard"""
    return render(request, 'bookings/book_cab.html', {
        'page_title': 'Book a Cab - CabGo'
    })

@login_required
@require_POST
def api_create_booking(request):
    """Backend endpoint to validate and save cab booking"""
    try:
        data = json.loads(request.body)
        
        pickup_address = data.get('pickup_address', '').strip()
        pickup_lat = float(data.get('pickup_latitude', 0))
        pickup_lng = float(data.get('pickup_longitude', 0))
        
        drop_address = data.get('drop_address', '').strip()
        drop_lat = float(data.get('drop_latitude', 0))
        drop_lng = float(data.get('drop_longitude', 0))
        
        distance_km = float(data.get('distance_km', 0))
        estimated_time = data.get('estimated_time', '15 min').strip()
        cab_type = data.get('cab_type', 'Sedan').strip()
        payment_method = data.get('payment_method', 'Cash').strip()

        # Validation
        if not pickup_address or not drop_address:
            return JsonResponse({'success': False, 'error': 'Pickup and Drop locations are required.'}, status=400)
        
        if distance_km <= 0:
            return JsonResponse({'success': False, 'error': 'Invalid trip distance. Please re-select locations.'}, status=400)

        # Fare Calculation logic (Server-side validation)
        base_fare = 50.00
        rate_map = {
            Booking.CAB_MINI: 10.00,
            Booking.CAB_SEDAN: 15.00,
            Booking.CAB_SUV: 20.00
        }
        per_km_rate = rate_map.get(cab_type, 15.00)
        fare = round(base_fare + (distance_km * per_km_rate), 2)

        # Pick random driver assignment
        driver = random.choice(DRIVER_POOL)

        booking = Booking.objects.create(
            user=request.user,
            pickup_address=pickup_address,
            pickup_latitude=pickup_lat,
            pickup_longitude=pickup_lng,
            drop_address=drop_address,
            drop_latitude=drop_lat,
            drop_longitude=drop_lng,
            distance_km=distance_km,
            estimated_time=estimated_time,
            cab_type=cab_type,
            base_fare=base_fare,
            per_km_rate=per_km_rate,
            fare=fare,
            payment_method=payment_method,
            booking_status=Booking.STATUS_CONFIRMED,
            driver_name=driver["name"],
            driver_vehicle=driver["vehicle"],
            driver_number=driver["number"],
            driver_phone=driver["phone"],
            driver_rating=driver["rating"]
        )

        return JsonResponse({
            'success': True,
            'booking_id': booking.booking_id,
            'redirect_url': f'/confirmation/{booking.booking_id}/'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def booking_confirmation_view(request, booking_id):
    """Booking receipt & real-time tracking confirmation screen"""
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, 'bookings/confirmation.html', {
        'booking': booking
    })

@login_required
def booking_history_view(request):
    """User's booking history list with filter support"""
    status_filter = request.GET.get('status', 'all').strip()
    
    bookings = Booking.objects.filter(user=request.user)
    
    if status_filter and status_filter.lower() != 'all':
        bookings = bookings.filter(booking_status__iexact=status_filter)

    return render(request, 'bookings/bookings_list.html', {
        'bookings': bookings,
        'current_status': status_filter
    })

@login_required
@require_POST
def api_cancel_booking(request, booking_id):
    """API endpoint to cancel an eligible booking"""
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    if not booking.is_cancellable:
        return JsonResponse({'success': False, 'error': f'Booking cannot be cancelled as it is already {booking.booking_status}.'}, status=400)
    
    booking.booking_status = Booking.STATUS_CANCELLED
    booking.save()
    
    return JsonResponse({
        'success': True,
        'message': f'Booking {booking.booking_id} cancelled successfully.'
    })

def register_view(request):
    """User Registration"""
    if request.user.is_authenticated:
        return redirect('book_cab')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome to CabGo, {user.first_name or user.username}.')
            return redirect('book_cab')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'bookings/register.html', {'form': form})

def login_view(request):
    """User Login"""
    if request.user.is_authenticated:
        return redirect('book_cab')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                next_url = request.GET.get('next', 'book_cab')
                return redirect(next_url)
        messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'bookings/login.html', {'form': form})

def logout_view(request):
    """User Logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
