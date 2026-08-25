from django.db import models
from restaurants.models import Restaurant

class Offer(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='offers', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.IntegerField(default=10, help_text="Percentage discount, e.g., 20 for 20%")
    coupon_code = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.coupon_code} - {self.discount_percentage}%)"
