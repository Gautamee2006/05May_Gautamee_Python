from django.contrib import admin
from .models import Profile, Address, OTPVerification, RecentlyViewed

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile', 'gender', 'city', 'state', 'pincode', 'created_at']
    search_fields = ['user__username', 'user__email', 'mobile', 'city']
    list_filter = ['gender', 'city', 'state']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'mobile', 'house_flat', 'city', 'address_type', 'is_default']
    search_fields = ['full_name', 'mobile', 'city', 'pincode']
    list_filter = ['address_type', 'is_default', 'state']

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'is_verified', 'created_at']
    search_fields = ['user__email', 'otp_code']
    list_filter = ['is_verified']

@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'viewed_at']
    search_fields = ['user__username', 'product__name']
