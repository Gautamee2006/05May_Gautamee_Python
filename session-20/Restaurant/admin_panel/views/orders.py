from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from orders.models import Order
from restaurants.models import Restaurant
from admin_panel.decorators import staff_required


ORDER_STATUS_PIPELINE = [
    'pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered'
]


@staff_required
def order_list(request):
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    date_filter = request.GET.get('date', '')

    orders = Order.objects.select_related('user').order_by('-created_at')

    if status_filter:
        orders = orders.filter(status=status_filter)
    if search:
        orders = orders.filter(order_number__icontains=search) | \
                 orders.filter(user__username__icontains=search)
    if date_filter:
        orders = orders.filter(created_at__date=date_filter)

    context = {
        'orders': orders[:100],
        'status_filter': status_filter,
        'search': search,
        'date_filter': date_filter,
        'status_choices': Order.STATUS_CHOICES,
        'page_title': 'Order Management',
        'active_nav': 'orders',
    }
    return render(request, 'admin_panel/orders/list.html', context)


@staff_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('user').prefetch_related('items'), pk=pk)

    # Determine next status in pipeline
    current_idx = ORDER_STATUS_PIPELINE.index(order.status) if order.status in ORDER_STATUS_PIPELINE else -1
    next_status = ORDER_STATUS_PIPELINE[current_idx + 1] if current_idx < len(ORDER_STATUS_PIPELINE) - 1 else None

    status_dict = dict(Order.STATUS_CHOICES)
    pipeline_steps = [(step, status_dict.get(step, step.replace('_', ' ').title())) for step in ORDER_STATUS_PIPELINE]

    context = {
        'order': order,
        'next_status': next_status,
        'status_choices': Order.STATUS_CHOICES,
        'pipeline_steps': pipeline_steps,
        'page_title': f'Order #{order.order_number}',
        'active_nav': 'orders',
    }
    return render(request, 'admin_panel/orders/detail.html', context)


@staff_required
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            old_status = order.status
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.order_number} status updated: {old_status} → {new_status}.")
        else:
            messages.error(request, "Invalid status.")
    return redirect('panel_order_detail', pk=pk)
