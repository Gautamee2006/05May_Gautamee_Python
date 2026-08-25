from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from orders.models import Order
from reservations.models import Reservation
from reviews.models import Review
from admin_panel.decorators import staff_required


@staff_required
def customer_list(request):
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    customers = User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')

    if search:
        customers = customers.filter(username__icontains=search) | \
                    customers.filter(email__icontains=search) | \
                    customers.filter(first_name__icontains=search)
    if status_filter == 'active':
        customers = customers.filter(is_active=True)
    elif status_filter == 'inactive':
        customers = customers.filter(is_active=False)

    context = {
        'customers': customers,
        'search': search,
        'status_filter': status_filter,
        'page_title': 'Customer Management',
        'active_nav': 'customers',
    }
    return render(request, 'admin_panel/customers/list.html', context)


@staff_required
def customer_detail(request, pk):
    customer = get_object_or_404(User, pk=pk, is_staff=False, is_superuser=False)
    orders = Order.objects.filter(user=customer).order_by('-created_at')[:10]
    reservations = Reservation.objects.filter(user=customer).order_by('-created_at')[:10]
    reviews = Review.objects.filter(user=customer).select_related('restaurant')[:10]

    context = {
        'customer': customer,
        'orders': orders,
        'reservations': reservations,
        'reviews': reviews,
        'page_title': f'Customer: {customer.get_full_name() or customer.username}',
        'active_nav': 'customers',
    }
    return render(request, 'admin_panel/customers/detail.html', context)


@staff_required
def customer_toggle(request, pk):
    customer = get_object_or_404(User, pk=pk, is_staff=False, is_superuser=False)
    if request.method == 'POST':
        customer.is_active = not customer.is_active
        customer.save()
        status = 'activated' if customer.is_active else 'deactivated'
        messages.success(request, f"Customer '{customer.username}' {status}.")
    return redirect('panel_customer_list')
