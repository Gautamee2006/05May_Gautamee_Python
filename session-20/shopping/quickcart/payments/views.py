from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import Payment

@login_required
def payment_gateway_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    payment = get_object_or_404(Payment, order=order)

    if payment.payment_status == 'Successful':
        return redirect('orders:order_success', order_id=order.order_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'success':
            payment.payment_status = 'Successful'
            payment.transaction_id = f"MOCK-TXN-{order.order_id}"
            payment.save()

            order.payment_status = 'Successful'
            order.order_status = 'Confirmed'
            order.save()

            messages.success(request, "Online payment completed successfully!")
            return redirect('orders:order_success', order_id=order.order_id)
        else:
            payment.payment_status = 'Failed'
            payment.save()

            order.payment_status = 'Failed'
            order.save()

            messages.error(request, "Payment transaction failed. Please try again or switch to COD.")
            return redirect('orders:order_detail', order_id=order.order_id)

    return render(request, 'payments/payment.html', {'order': order, 'payment': payment})
