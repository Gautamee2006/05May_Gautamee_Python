from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f"OTP for {user_str} ({self.phone_number}) - Verified: {self.is_verified}"

    def is_expired(self):
        """Check if the OTP has passed its expiry time."""
        return timezone.now() > self.expires_at

    def is_valid(self):
        """Check if OTP is valid for verification (not verified, not expired, under attempt limit)."""
        return not self.is_verified and not self.is_expired() and self.attempts < 5
