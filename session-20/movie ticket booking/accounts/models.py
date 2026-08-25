from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
import random

class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp_verification')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    def generate_new_otp(self):
        new_otp = str(random.randint(100000, 999999))
        self.otp = new_otp
        self.created_at = timezone.now()
        self.expires_at = timezone.now() + datetime.timedelta(minutes=3)
        self.is_verified = False
        self.attempts = 0
        self.save()
        return new_otp

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP for {self.user.email} - {'Verified' if self.is_verified else 'Pending'}"
