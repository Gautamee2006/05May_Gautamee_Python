from django.contrib import admin
from django.contrib.auth.models import User
from .models import Movie, Show, Booking

# Customizing default admin site headers
admin.site.site_header = "Movie Ticket Booking Admin Panel"
admin.site.site_title = "Admin Dashboard"
admin.site.index_title = "Control Panel & Summary Statistics"

# Inject summary statistics into admin index context
original_index = admin.site.index

def custom_admin_index(request, extra_context=None):
    extra = extra_context or {}
    extra['total_users'] = User.objects.count()
    extra['total_movies'] = Movie.objects.count()
    extra['total_shows'] = Show.objects.count()
    extra['total_bookings'] = Booking.objects.count()
    extra['confirmed_bookings'] = Booking.objects.filter(status='Confirmed').count()
    extra['cancelled_bookings'] = Booking.objects.filter(status='Cancelled').count()
    return original_index(request, extra_context=extra)

admin.site.index = custom_admin_index


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'duration', 'release_date', 'rating')
    list_filter = ('genre', 'language')
    search_fields = ('title', 'description')
    ordering = ('title',)


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie', 'date', 'time', 'screen_name', 'ticket_price')
    list_filter = ('date', 'screen_name', 'movie__genre', 'movie__language')
    search_fields = ('movie__title', 'screen_name')
    ordering = ('-date', 'time')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'movie', 'show', 'selected_seats', 'total_amount', 'booking_date', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('booking_id', 'user__email', 'user__username', 'selected_seats')
    readonly_fields = ('booking_id', 'booking_date')
    ordering = ('-booking_date',)
    list_editable = ('status',)
