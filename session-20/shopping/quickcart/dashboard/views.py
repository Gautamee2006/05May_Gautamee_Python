from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from products.models import Product, Category, Review
from products.forms import ProductForm, CategoryForm
from orders.models import Order, ReturnRequest
from coupons.models import Coupon
from coupons.forms import CouponForm
from support.models import SupportTicket

@staff_member_required
def dashboard_home_view(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    
    successful_orders = Order.objects.filter(payment_status='Successful')
    total_revenue = successful_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    pending_orders = Order.objects.filter(order_status='Placed').count()
    delivered_orders = Order.objects.filter(order_status='Delivered').count()
    cancelled_orders = Order.objects.filter(order_status='Cancelled').count()
    low_stock_products = Product.objects.filter(stock__lte=5)

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'low_stock_count': low_stock_products.count(),
        'low_stock_products': low_stock_products[:5],
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/dashboard.html', context)


@staff_member_required
def dashboard_products_view(request):
    products = Product.objects.select_related('category').order_by('-created_at')
    categories = Category.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_product':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Product added successfully!")
                return redirect('dashboard:products')
            else:
                messages.error(request, "Error adding product.")
        elif action == 'add_category':
            c_form = CategoryForm(request.POST, request.FILES)
            if c_form.is_valid():
                c_form.save()
                messages.success(request, "Category added successfully!")
                return redirect('dashboard:products')

    product_form = ProductForm()
    category_form = CategoryForm()

    context = {
        'products': products,
        'categories': categories,
        'product_form': product_form,
        'category_form': category_form,
    }
    return render(request, 'dashboard/products.html', context)


@staff_member_required
def dashboard_edit_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated '{product.name}' successfully.")
            return redirect('dashboard:products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'dashboard/edit_product.html', {'form': form, 'product': product})


@staff_member_required
def dashboard_delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    name = product.name
    product.delete()
    messages.info(request, f"Deleted product '{name}'.")
    return redirect('dashboard:products')


@staff_member_required
def dashboard_orders_view(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(order_status=status_filter)

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('order_status')
        order = get_object_or_404(Order, id=order_id)
        order.order_status = new_status
        order.save()
        messages.success(request, f"Order #{order.order_id} status updated to '{new_status}'.")
        return redirect('dashboard:orders')

    return render(request, 'dashboard/orders.html', {'orders': orders, 'current_filter': status_filter})


@staff_member_required
def dashboard_users_view(request):
    users = User.objects.select_related('profile').order_by('-date_joined')
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user_obj = get_object_or_404(User, id=user_id)
        
        if action == 'toggle_active':
            user_obj.is_active = not user_obj.is_active
            user_obj.save()
            state = "activated" if user_obj.is_active else "deactivated"
            messages.success(request, f"User '{user_obj.username}' has been {state}.")
            return redirect('dashboard:users')

    return render(request, 'dashboard/users.html', {'users': users})


@staff_member_required
def dashboard_inventory_view(request):
    products = Product.objects.all().order_by('stock')
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        new_stock = request.POST.get('stock')
        if product_id and new_stock is not None:
            product = get_object_or_404(Product, id=product_id)
            product.stock = int(new_stock)
            product.save()
            messages.success(request, f"Stock updated for {product.name} to {new_stock} units.")
            return redirect('dashboard:inventory')

    return render(request, 'dashboard/inventory.html', {'products': products})


@staff_member_required
def dashboard_coupons_view(request):
    coupons = Coupon.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New coupon created successfully!")
            return redirect('dashboard:coupons')
    else:
        form = CouponForm()

    return render(request, 'dashboard/coupons.html', {'coupons': coupons, 'form': form})


@staff_member_required
def dashboard_delete_coupon_view(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    code = coupon.code
    coupon.delete()
    messages.info(request, f"Deleted coupon '{code}'.")
    return redirect('dashboard:coupons')


@staff_member_required
def dashboard_tickets_view(request):
    tickets = SupportTicket.objects.select_related('user').order_by('-created_at')
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        new_status = request.POST.get('status')
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        ticket.status = new_status
        ticket.save()
        messages.success(request, f"Ticket #{ticket.ticket_id} status set to '{new_status}'.")
        return redirect('dashboard:tickets')

    return render(request, 'dashboard/tickets.html', {'tickets': tickets})
