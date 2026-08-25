from django.contrib import admin
from .models import OTPVerification

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at', 'expires_at', 'is_verified', 'attempts')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username', 'user__email', 'otp')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
