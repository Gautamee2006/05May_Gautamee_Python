from django.contrib import admin
from .models import Coupon, CouponUsage

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'min_order_amount', 'expiry_date', 'usage_limit', 'is_active']
    list_filter = ['discount_type', 'is_active', 'expiry_date']
    search_fields = ['code']

@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'user', 'used_at']
    search_fields = ['coupon__code', 'user__username']
