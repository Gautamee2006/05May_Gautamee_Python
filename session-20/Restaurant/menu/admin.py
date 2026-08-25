from django.contrib import admin
from .models import MenuCategory, FoodItem

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'order']
    list_filter = ['restaurant']
    search_fields = ['name', 'restaurant__name']

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'category', 'price', 'is_vegetarian', 'is_available']
    list_filter = ['restaurant', 'category', 'is_vegetarian', 'is_available']
    search_fields = ['name', 'description', 'restaurant__name']
