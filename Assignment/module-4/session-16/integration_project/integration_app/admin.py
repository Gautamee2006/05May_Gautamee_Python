from django.contrib import admin
from integration_app.models import OTPVerification

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    # Hide raw OTP from list_display for security
    list_display = ('user', 'phone_number', 'created_at', 'expires_at', 'is_verified', 'attempts')
    list_filter = ('is_verified', 'created_at', 'expires_at')
    search_fields = ('phone_number', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'masked_otp')
    exclude = ('otp',)

    def masked_otp(self, obj):
        if obj.otp:
            return f"***{obj.otp[-2:]}" if len(obj.otp) >= 2 else "******"
        return "N/A"
    masked_otp.short_description = "OTP Code (Masked)"
