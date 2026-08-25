from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from cart.models import CartItem
from accounts.models import Address
from products.models import Product
from coupons.models import Coupon, CouponUsage
from notifications.models import Notification
from payments.models import Payment
from .models import Order, OrderItem, ReturnRequest
from .forms import ReturnRequestForm

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    if not cart_items.exists():
        messages.warning(request, "Your shopping cart is empty.")
        return redirect('cart:cart')

    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    
    # Check stock limits
    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f"Sorry, '{item.product.name}' has only {item.product.stock} items available.")
            return redirect('cart:cart')

    subtotal = sum(item.original_total_price for item in cart_items)
    product_discount = sum(item.total_discount for item in cart_items)
    price_after_product_discount = subtotal - product_discount

    delivery_charge = Decimal('0.00') if price_after_product_discount > Decimal('500.00') else Decimal('50.00')

    coupon_code = request.session.get('applied_coupon')
    coupon_discount = Decimal('0.00')
    applied_coupon_obj = None

    if coupon_code:
        coupon = Coupon.objects.filter(code=coupon_code, is_active=True).first()
        if coupon and coupon.is_valid() and price_after_product_discount >= coupon.min_order_amount:
            coupon_discount = coupon.calculate_discount(price_after_product_discount)
            applied_coupon_obj = coupon

    final_total = max(Decimal('0.00'), price_after_product_discount - coupon_discount + delivery_charge)

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        payment_method = request.POST.get('payment_method', 'COD')

        if not address_id:
            messages.error(request, "Please select or add a delivery address.")
            return redirect('orders:checkout')

        address = get_object_or_404(Address, id=address_id, user=request.user)

        # Snapshot address
        address_text = f"{address.full_name}, Phone: {address.mobile}\n{address.house_flat}, {address.street}, {address.area}\n{address.city}, {address.state} - {address.pincode} ({address.address_type})"

        # Create Order
        order = Order.objects.create(
            user=request.user,
            address=address,
            address_snapshot=address_text,
            total_amount=final_total,
            discount=product_discount + coupon_discount,
            delivery_charge=delivery_charge,
            payment_status='Pending' if payment_method == 'Online' else 'Successful',
            order_status='Placed'
        )

        # Create Order Items and reduce stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
                discount=item.product.price - item.product.final_price,
                final_price=item.product.final_price
            )
            # Deduct stock
            item.product.stock -= item.quantity
            item.product.save()

        # Record Coupon Usage
        if applied_coupon_obj:
            CouponUsage.objects.create(coupon=applied_coupon_obj, user=request.user)
            del request.session['applied_coupon']

        # Create Payment object
        payment = Payment.objects.create(
            order=order,
            amount=final_total,
            payment_method=payment_method,
            payment_status='Pending' if payment_method == 'Online' else 'Successful',
            transaction_id=f"TXN-{order.order_id}"
        )

        # Clear cart
        cart_items.delete()

        # Notification
        Notification.objects.create(
            user=request.user,
            title="Order Placed Successfully",
            message=f"Your order #{order.order_id} has been placed successfully for ₹{final_total}."
        )

        if payment_method == 'Online':
            return redirect('payments:payment_gateway', order_id=order.order_id)
        else:
            messages.success(request, f"Order #{order.order_id} placed successfully with Cash on Delivery!")
            return redirect('orders:order_success', order_id=order.order_id)

    context = {
        'cart_items': cart_items,
        'addresses': addresses,
        'subtotal': subtotal,
        'product_discount': product_discount,
        'delivery_charge': delivery_charge,
        'coupon_discount': coupon_discount,
        'final_total': final_total,
        'applied_coupon': applied_coupon_obj,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    status_filter = request.GET.get('status')

    if status_filter:
        orders = orders.filter(order_status=status_filter)

    return render(request, 'orders/my_orders.html', {'orders': orders, 'current_filter': status_filter})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    items = order.items.all()
    return render(request, 'orders/order_detail.html', {'order': order, 'items': items})


@login_required
def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if not order.can_cancel():
        messages.error(request, "This order cannot be cancelled as it has already been shipped/delivered.")
        return redirect('orders:order_detail', order_id=order.order_id)

    order.order_status = 'Cancelled'
    if order.payment_status == 'Successful':
        order.payment_status = 'Refunded'
        if hasattr(order, 'payment'):
            order.payment.payment_status = 'Refunded'
            order.payment.save()
    order.save()

    # Restore product stock
    for item in order.items.all():
        if item.product:
            item.product.stock += item.quantity
            item.product.save()

    Notification.objects.create(
        user=request.user,
        title="Order Cancelled",
        message=f"Your order #{order.order_id} has been cancelled successfully."
    )

    messages.info(request, f"Order #{order.order_id} has been cancelled.")
    return redirect('orders:order_detail', order_id=order.order_id)


@login_required
def return_product_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)

    if not order.can_return():
        messages.error(request, "Return is not available for this order.")
        return redirect('orders:order_detail', order_id=order.order_id)

    if request.method == 'POST':
        form = ReturnRequestForm(request.POST)
        if form.is_valid():
            return_req = form.save(commit=False)
            return_req.order = order
            return_req.status = 'Requested'
            return_req.save()

            order.order_status = 'Returned'
            order.save()

            Notification.objects.create(
                user=request.user,
                title="Return Requested",
                message=f"Return request submitted for Order #{order.order_id}."
            )

            messages.success(request, "Your return request has been submitted successfully.")
            return redirect('orders:order_detail', order_id=order.order_id)
    else:
        form = ReturnRequestForm()

    return render(request, 'orders/return_product.html', {'form': form, 'order': order})


@login_required
def invoice_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    # Security check: User must own the order or be staff/admin
    if order.user != request.user and not request.user.is_staff:
        messages.error(request, "Unauthorized access to invoice.")
        return redirect('home')

    items = order.items.all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'orders/invoice.html', context)
