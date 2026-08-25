from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'order', 'amount', 'payment_method', 'payment_status', 'created_at']
    list_filter = ['payment_method', 'payment_status']
    search_fields = ['payment_id', 'order__order_id', 'transaction_id']
