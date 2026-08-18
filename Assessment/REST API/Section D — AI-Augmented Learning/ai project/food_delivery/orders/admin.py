from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'item', 'quantity')
    search_fields = ('customer_name', 'item')
    list_filter = ('customer_name', 'item')
