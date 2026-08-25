from django.contrib import admin
from .models import Order, OrderItem, ReturnRequest

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'total_amount', 'payment_status', 'order_status', 'created_at']
    list_filter = ['order_status', 'payment_status', 'created_at']
    search_fields = ['order_id', 'user__username', 'user__email']
    inlines = [OrderItemInline]

@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ['order', 'reason', 'status', 'created_at']
    list_filter = ['status', 'reason']
    search_fields = ['order__order_id', 'description']
