from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodItem

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    coupon_code = models.CharField(max_length=50, null=True, blank=True)
    discount_percentage = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.id} ({self.user.username if self.user else self.session_id})"

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def discount_amount(self):
        if self.discount_percentage > 0:
            return round((self.subtotal * self.discount_percentage) / 100, 2)
        return 0

    @property
    def delivery_fee(self):
        return 40.00 if self.subtotal > 0 else 0.00

    @property
    def total(self):
        return max(0, float(self.subtotal) - float(self.discount_amount) + float(self.delivery_fee))

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"

    @property
    def subtotal(self):
        return self.food_item.price * self.quantity
