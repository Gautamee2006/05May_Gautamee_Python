from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from menu.models import FoodItem
from offers.models import Offer
from .models import Cart, CartItem
from datetime import date

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_id=session_id)
    return cart

@login_required(login_url='login')
def add_to_cart_view(request, food_item_id):
    if request.method == 'POST':
        food_item = get_object_or_404(FoodItem, id=food_item_id, is_available=True)
        quantity = int(request.POST.get('quantity', 1))
        
        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        messages.success(request, f"Added {quantity} x '{food_item.name}' to your cart! 🍕")

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else 'cart_detail')

@login_required(login_url='login')
def update_cart_item_view(request, item_id):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        action = request.POST.get('action')

        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
                messages.info(request, f"Removed '{cart_item.food_item.name}' from cart.")

    return redirect('cart_detail')

@login_required(login_url='login')
def remove_cart_item_view(request, item_id):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        name = cart_item.food_item.name
        cart_item.delete()
        messages.info(request, f"Removed '{name}' from your cart.")
    return redirect('cart_detail')

@login_required(login_url='login')
def clear_cart_view(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        cart.coupon_code = None
        cart.discount_percentage = 0
        cart.save()
        messages.info(request, "Your cart has been cleared.")
    return redirect('cart_detail')

@login_required(login_url='login')
def apply_coupon_view(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip().upper()
        cart = get_or_create_cart(request)

        if not code:
            cart.coupon_code = None
            cart.discount_percentage = 0
            cart.save()
            messages.info(request, "Coupon removed.")
            return redirect('cart_detail')

        offer = Offer.objects.filter(coupon_code__iexact=code, is_active=True, end_date__gte=date.today()).first()
        if offer:
            cart.coupon_code = offer.coupon_code
            cart.discount_percentage = offer.discount_percentage
            cart.save()
            messages.success(request, f"Coupon '{offer.coupon_code}' applied! You saved {offer.discount_percentage}%! 🎉")
        else:
            messages.error(request, "Invalid or expired coupon code.")

    return redirect('cart_detail')

@login_required(login_url='login')
def cart_detail_view(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.select_related('food_item', 'food_item__restaurant').all()
    active_offers = Offer.objects.filter(is_active=True, end_date__gte=date.today())[:3]

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'active_offers': active_offers,
    }
    return render(request, 'cart/cart_detail.html', context)
