from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from products.models import Product
from .models import CartItem, Wishlist
from coupons.models import Coupon

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    
    subtotal = sum(item.original_total_price for item in cart_items)
    product_discount = sum(item.total_discount for item in cart_items)
    price_after_product_discount = subtotal - product_discount

    delivery_charge = Decimal('0.00') if price_after_product_discount > Decimal('500.00') or price_after_product_discount == 0 else Decimal('50.00')

    coupon_code = request.session.get('applied_coupon')
    coupon_discount = Decimal('0.00')
    applied_coupon_obj = None

    if coupon_code:
        coupon = Coupon.objects.filter(code=coupon_code, is_active=True).first()
        if coupon and coupon.is_valid():
            if price_after_product_discount >= coupon.min_order_amount:
                coupon_discount = coupon.calculate_discount(price_after_product_discount)
                applied_coupon_obj = coupon
            else:
                del request.session['applied_coupon']
                messages.warning(request, f"Coupon '{coupon_code}' removed: minimum order amount is ₹{coupon.min_order_amount}.")
        else:
            del request.session['applied_coupon']

    final_total = max(Decimal('0.00'), price_after_product_discount - coupon_discount + delivery_charge)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'product_discount': product_discount,
        'price_after_product_discount': price_after_product_discount,
        'delivery_charge': delivery_charge,
        'coupon_discount': coupon_discount,
        'applied_coupon': applied_coupon_obj,
        'final_total': final_total,
    }
    return render(request, 'cart/cart.html', context)


@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect('products:product_detail', slug=product.slug)

    requested_qty = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': requested_qty}
    )

    if not created:
        new_qty = cart_item.quantity + requested_qty
        if new_qty > product.stock:
            cart_item.quantity = product.stock
            cart_item.save()
            messages.warning(request, f"Set quantity to maximum available stock ({product.stock}).")
        else:
            cart_item.quantity = new_qty
            cart_item.save()
            messages.success(request, f"Updated {product.name} quantity in cart.")
    else:
        if requested_qty > product.stock:
            cart_item.quantity = product.stock
            cart_item.save()
            messages.warning(request, f"Only {product.stock} items available in stock.")
        else:
            messages.success(request, f"Added {product.name} to your cart.")

    action = request.POST.get('action')
    if action == 'buy_now':
        return redirect('orders:checkout')

    return redirect('cart:cart')


@login_required
def update_cart_view(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        if cart_item.quantity + 1 > cart_item.product.stock:
            messages.error(request, f"Only {cart_item.product.stock} units available in stock.")
        else:
            cart_item.quantity += 1
            cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity - 1 <= 0:
            cart_item.delete()
            messages.info(request, f"Removed {cart_item.product.name} from cart.")
            return redirect('cart:cart')
        else:
            cart_item.quantity -= 1
            cart_item.save()

    return redirect('cart:cart')


@login_required
def remove_from_cart_view(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"Removed {product_name} from your cart.")
    return redirect('cart:cart')


@login_required
def clear_cart_view(request):
    CartItem.objects.filter(user=request.user).delete()
    messages.info(request, "Your shopping cart has been cleared.")
    return redirect('cart:cart')


# --- Wishlist Views ---
@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'cart/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def toggle_wishlist_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist_item.delete()
        messages.info(request, f"Removed {product.name} from your wishlist.")
    else:
        messages.success(request, f"Added {product.name} to your wishlist!")

    next_url = request.META.get('HTTP_REFERER') or 'cart:wishlist'
    return redirect(next_url)


@login_required
def remove_from_wishlist_view(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    messages.info(request, "Item removed from wishlist.")
    return redirect('cart:wishlist')


@login_required
def move_wishlist_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    if product.stock <= 0:
        messages.error(request, f"Sorry, {product.name} is out of stock.")
        return redirect('cart:wishlist')

    CartItem.objects.get_or_create(user=request.user, product=product, defaults={'quantity': 1})
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f"Moved {product.name} from wishlist to cart.")
    return redirect('cart:cart')
