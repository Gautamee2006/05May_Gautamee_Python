from django.contrib import admin
from .models import Restaurant

from django.contrib import admin
from .models import Restaurant

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'cuisine', 'rating']
    search_fields = ['name', 'cuisine']
    list_filter = ['cuisine', 'rating']

admin.site.register(Restaurant, RestaurantAdmin)