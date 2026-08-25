import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem

@login_required
def checkout_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty. Add food items before checkout!")
        return redirect('restaurant_list')

    profile = request.user.profile

    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', '').strip()
        phone = request.POST.get('phone', '').strip()
        payment_method = request.POST.get('payment_method', 'Cash on Delivery')

        if not delivery_address or not phone:
            messages.error(request, "Please fill in all delivery details.")
            return redirect('checkout')

        # Generate unique order number
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            total_amount=cart.subtotal,
            discount_amount=cart.discount_amount,
            final_amount=cart.total,
            status='pending',
            delivery_address=delivery_address,
            phone=phone,
            payment_method=payment_method
        )

        # Create OrderItems
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                food_item=cart_item.food_item,
                food_name=cart_item.food_item.name,
                quantity=cart_item.quantity,
                price=cart_item.food_item.price,
                subtotal=cart_item.subtotal
            )

        # Clear cart after successful order creation
        cart.items.all().delete()
        cart.coupon_code = None
        cart.discount_percentage = 0
        cart.save()

        messages.success(request, f"Order placed successfully! Order #{order.order_number}")
        return redirect('order_confirmation', order_id=order.id)

    context = {
        'cart': cart,
        'profile': profile,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation.html', {'order': order})

@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def cancel_order_view(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            messages.info(request, f"Order #{order.order_number} has been cancelled.")
        else:
            messages.warning(request, "This order cannot be cancelled as it is already being prepared or out for delivery.")
    return redirect('order_detail', order_id=order_id)
