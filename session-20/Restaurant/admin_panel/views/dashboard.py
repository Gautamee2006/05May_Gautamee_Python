from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from django.contrib.auth.models import User
from restaurants.models import Restaurant
from orders.models import Order, OrderItem
from reservations.models import Reservation
from reviews.models import Review
from admin_panel.decorators import staff_required


@staff_required
def dashboard_view(request):
    today = timezone.localdate()

    # Core stats
    total_restaurants = Restaurant.objects.filter(is_active=True).count()
    total_customers = User.objects.filter(is_staff=False, is_superuser=False).count()
    total_orders_today = Order.objects.filter(created_at__date=today).count()
    total_reservations_today = Reservation.objects.filter(date=today).count()
    pending_orders = Order.objects.filter(status='pending').count()
    pending_reservations = Reservation.objects.filter(status='pending').count()
    avg_rating = Restaurant.objects.aggregate(avg=Avg('rating'))['avg'] or 0

    # Revenue
    revenue_today = Order.objects.filter(
        created_at__date=today, status='delivered'
    ).aggregate(total=Sum('final_amount'))['total'] or 0

    total_revenue = Order.objects.filter(
        status='delivered'
    ).aggregate(total=Sum('final_amount'))['total'] or 0

    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]

    # Recent reservations
    recent_reservations = Reservation.objects.select_related(
        'user', 'restaurant'
    ).order_by('-created_at')[:8]

    # Popular restaurant (by order count via food items)
    popular_restaurant = Restaurant.objects.annotate(
        order_count=Count('food_items__orderitem')
    ).order_by('-order_count').first()

    # Most ordered food
    most_ordered_food = OrderItem.objects.values(
        'food_name'
    ).annotate(count=Count('id')).order_by('-count').first()

    context = {
        'total_restaurants': total_restaurants,
        'total_customers': total_customers,
        'total_orders_today': total_orders_today,
        'total_reservations_today': total_reservations_today,
        'pending_orders': pending_orders,
        'pending_reservations': pending_reservations,
        'avg_rating': round(avg_rating, 2),
        'revenue_today': revenue_today,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'recent_reservations': recent_reservations,
        'popular_restaurant': popular_restaurant,
        'most_ordered_food': most_ordered_food,
        'page_title': 'Dashboard',
        'active_nav': 'dashboard',
    }
    return render(request, 'admin_panel/dashboard.html', context)
