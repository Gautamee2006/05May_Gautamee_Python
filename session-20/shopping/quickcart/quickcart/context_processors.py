from products.models import Category
from cart.models import CartItem, Wishlist
from notifications.models import Notification

def global_ecommerce_context(request):
    categories = Category.objects.all()
    cart_count = 0
    wishlist_count = 0
    unread_notifications_count = 0

    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return {
        'nav_categories': categories,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'unread_notifications_count': unread_notifications_count,
    }
