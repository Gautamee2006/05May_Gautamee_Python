from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Coupon(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage Discount (%)'),
        ('fixed', 'Fixed Discount (₹)'),
    )

    code = models.CharField(max_length=30, unique=True)
    discount_type = models.CharField(max_length=15, choices=DISCOUNT_TYPES, default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField()
    usage_limit = models.PositiveIntegerField(default=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        today = timezone.now().date()
        if not self.is_active:
            return False
        if self.start_date > today or self.expiry_date < today:
            return False
        if self.usages.count() >= self.usage_limit:
            return False
        return True

    def calculate_discount(self, amount):
        if self.discount_type == 'percentage':
            discount = Decimal(amount) * (Decimal(self.discount_value) / Decimal(100))
            if self.max_discount:
                discount = min(discount, Decimal(self.max_discount))
            return discount.quantize(Decimal('0.01'))
        else:
            return min(Decimal(self.discount_value), Decimal(amount)).quantize(Decimal('0.01'))

    def __str__(self):
        return f"{self.code} ({self.get_discount_type_display()})"


class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_usages')
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} used {self.coupon.code}"
