from django.contrib import admin
from .models import Location, Cuisine, Restaurant, SearchHistory

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'state', 'is_active']
    list_filter = ['is_active', 'state']
    search_fields = ['name', 'state']

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'cuisine', 'location', 'rating', 'price_range', 'opening_time', 'closing_time', 'is_active']
    list_filter = ['cuisine', 'location', 'price_range', 'is_active']
    search_fields = ['name', 'address', 'description']

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'query']
