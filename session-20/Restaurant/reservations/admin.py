from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'restaurant', 'date', 'time', 'num_people', 'status', 'created_at']
    list_filter = ['status', 'date', 'restaurant']
    search_fields = ['user__username', 'restaurant__name', 'special_request']
    list_editable = ['status']
