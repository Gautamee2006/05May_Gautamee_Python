from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from orders.models import Order, OrderItem
from restaurants.models import Restaurant, Cuisine
from reservations.models import Reservation
from admin_panel.decorators import staff_required


@staff_required
def analytics_view(request):
    today = timezone.localdate()
    this_month_start = today.replace(day=1)

    # Revenue stats
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('final_amount'))['total'] or 0
    today_revenue = Order.objects.filter(
        status='delivered', created_at__date=today
    ).aggregate(total=Sum('final_amount'))['total'] or 0
    month_revenue = Order.objects.filter(
        status='delivered', created_at__date__gte=this_month_start
    ).aggregate(total=Sum('final_amount'))['total'] or 0

    # Order stats by status
    order_status_counts = {}
    for status, label in Order.STATUS_CHOICES:
        order_status_counts[label] = Order.objects.filter(status=status).count()

    total_orders = sum(order_status_counts.values())

    # Popular restaurants (by number of food item orders)
    popular_restaurants = Restaurant.objects.annotate(
        order_count=Count('food_items__orderitem')
    ).filter(is_active=True).order_by('-order_count')[:5]

    # Most ordered food items
    top_food_items = OrderItem.objects.values('food_name').annotate(
        count=Count('id'),
        revenue=Sum('subtotal')
    ).order_by('-count')[:10]

    # Most popular cuisines
    popular_cuisines = Cuisine.objects.annotate(
        restaurant_count=Count('restaurants'),
        order_count=Count('restaurants__food_items__orderitem')
    ).order_by('-order_count')[:6]

    # Reservation stats
    total_reservations = Reservation.objects.count()
    pending_reservations = Reservation.objects.filter(status='pending').count()
    confirmed_reservations = Reservation.objects.filter(status='confirmed').count()

    # Orders by month (last 6 months simple count)
    monthly_orders = []
    for i in range(5, -1, -1):
        import calendar
        d = today.replace(day=1)
        # Go back i months
        month = d.month - i
        year = d.year
        while month <= 0:
            month += 12
            year -= 1
        month_name = calendar.month_abbr[month]
        count = Order.objects.filter(
            created_at__year=year, created_at__month=month
        ).count()
        monthly_orders.append({'month': month_name, 'count': count})

    context = {
        'total_revenue': total_revenue,
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'order_status_counts': order_status_counts,
        'total_orders': total_orders,
        'popular_restaurants': popular_restaurants,
        'top_food_items': top_food_items,
        'popular_cuisines': popular_cuisines,
        'total_reservations': total_reservations,
        'pending_reservations': pending_reservations,
        'confirmed_reservations': confirmed_reservations,
        'monthly_orders': monthly_orders,
        'page_title': 'Analytics & Insights',
        'active_nav': 'analytics',
    }
    return render(request, 'admin_panel/analytics/index.html', context)
