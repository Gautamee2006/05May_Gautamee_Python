from django.contrib import admin
from .models import SupportTicket, FAQ

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user', 'category', 'subject', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['ticket_id', 'user__username', 'subject', 'message']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
