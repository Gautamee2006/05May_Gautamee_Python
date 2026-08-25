from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_id',
        'user',
        'cab_type',
        'distance_km',
        'fare',
        'payment_method',
        'booking_status',
        'driver_name',
        'created_at'
    )
    list_filter = ('booking_status', 'cab_type', 'payment_method', 'created_at')
    search_fields = (
        'booking_id',
        'user__username',
        'user__email',
        'pickup_address',
        'drop_address',
        'driver_name',
        'driver_vehicle'
    )
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    fieldsets = (
        ('Booking Reference', {
            'fields': ('booking_id', 'user', 'booking_status', 'created_at', 'updated_at')
        }),
        ('Location Information', {
            'fields': ('pickup_address', 'pickup_latitude', 'pickup_longitude', 'drop_address', 'drop_latitude', 'drop_longitude')
        }),
        ('Ride & Pricing Details', {
            'fields': ('cab_type', 'distance_km', 'estimated_time', 'base_fare', 'per_km_rate', 'fare', 'payment_method')
        }),
        ('Driver Information', {
            'fields': ('driver_name', 'driver_vehicle', 'driver_number', 'driver_phone', 'driver_rating', 'user_rating')
        }),
    )

    actions = ['mark_completed', 'mark_cancelled', 'mark_on_the_way']

    @admin.action(description="Mark selected bookings as Completed")
    def mark_completed(self, request, queryset):
        queryset.update(booking_status=Booking.STATUS_COMPLETED)
        self.message_user(request, "Selected bookings updated to Completed.")

    @admin.action(description="Mark selected bookings as Cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(booking_status=Booking.STATUS_CANCELLED)
        self.message_user(request, "Selected bookings updated to Cancelled.")

    @admin.action(description="Mark selected bookings as On the Way")
    def mark_on_the_way(self, request, queryset):
        queryset.update(booking_status=Booking.STATUS_ON_THE_WAY)
        self.message_user(request, "Selected bookings updated to On the Way.")
