from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm
from restaurants.models import Restaurant, SearchHistory
from favorites.models import Favorite
from orders.models import Order
from reservations.models import Reservation

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = user.profile
            profile.mobile = form.cleaned_data['mobile']
            profile.save()

            login(request, user)
            messages.success(request, f"Welcome to TasteTrail, {user.first_name}! Account created successfully.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the registration errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                next_url = request.GET.get('next') or 'home'
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('home')
    return redirect('home')

@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Please fix the errors in your profile form.")
    else:
        form = UserProfileForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'mobile': profile.mobile,
            'address': profile.address,
            'city': profile.city,
        })

    return render(request, 'accounts/profile.html', {'form': form, 'user_obj': user})

@login_required
def dashboard_view(request):
    user = request.user
    favorites_count = Favorite.objects.filter(user=user).count()
    orders_count = Order.objects.filter(user=user).count()
    reservations_count = Reservation.objects.filter(user=user).count()

    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    upcoming_reservations = Reservation.objects.filter(user=user).order_by('-date', '-time')[:5]
    recent_searches = SearchHistory.objects.filter(user=user).order_by('-created_at')[:5]

    # Track recently viewed restaurants from session
    recently_viewed_ids = request.session.get('recently_viewed', [])
    recently_viewed_restaurants = Restaurant.objects.filter(id__in=recently_viewed_ids)

    context = {
        'favorites_count': favorites_count,
        'orders_count': orders_count,
        'reservations_count': reservations_count,
        'recent_orders': recent_orders,
        'upcoming_reservations': upcoming_reservations,
        'recent_searches': recent_searches,
        'recently_viewed_restaurants': recently_viewed_restaurants,
    }
    return render(request, 'accounts/dashboard.html', context)
