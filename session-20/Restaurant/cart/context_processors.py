from cart.models import Cart

def cart_context(request):
    cart_count = 0
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        if request.session.session_key:
            cart = Cart.objects.filter(session_id=request.session.session_key).first()
    
    if cart:
        cart_count = sum(item.quantity for item in cart.items.all())
    
    return {
        'cart_count': cart_count,
        'cart_obj': cart
    }
