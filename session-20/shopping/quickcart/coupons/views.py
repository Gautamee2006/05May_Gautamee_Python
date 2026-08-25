from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Coupon
from cart.models import CartItem
from decimal import Decimal

@login_required
def apply_coupon_view(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        coupon = Coupon.objects.filter(code__iexact=code).first()

        if not coupon:
            messages.error(request, f"Invalid coupon code '{code}'.")
            return redirect('cart:cart')

        if not coupon.is_valid():
            messages.error(request, f"Coupon '{code}' is expired or inactive.")
            return redirect('cart:cart')

        cart_items = CartItem.objects.filter(user=request.user)
        subtotal = sum(item.total_price for item in cart_items)

        if subtotal < coupon.min_order_amount:
            messages.error(request, f"Coupon requires a minimum order amount of ₹{coupon.min_order_amount}.")
            return redirect('cart:cart')

        request.session['applied_coupon'] = coupon.code
        messages.success(request, f"Coupon '{coupon.code}' applied successfully!")

    return redirect('cart:cart')


@login_required
def remove_coupon_view(request):
    if 'applied_coupon' in request.session:
        del request.session['applied_coupon']
        messages.info(request, "Coupon removed from cart.")
    return redirect('cart:cart')


def coupons_list_view(request):
    today = timezone.now().date()
    available_coupons = Coupon.objects.filter(
        is_active=True,
        start_date__lte=today,
        expiry_date__gte=today
    )
    return render(request, 'coupons/coupons.html', {'coupons': available_coupons})
