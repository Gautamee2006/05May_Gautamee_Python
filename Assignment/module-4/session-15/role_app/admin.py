from django.contrib import admin
from .models import Order, Product, Movie, Review, Playlist


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_name', 'price', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'product_name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'seller', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'seller__username')


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_date')
    search_fields = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('movie__title', 'user__username')


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'created_at')
    search_fields = ('name', 'created_by__username')

    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()

    def has_add_permission(self, request):
        return request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()
