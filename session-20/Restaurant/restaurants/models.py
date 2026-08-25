from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, time

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    state = models.CharField(max_length=100, blank=True, default='Gujarat')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Cuisine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, default='fa-utensils')
    image = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    PRICE_CHOICES = [
        ('$', 'Budget ($)'),
        ('$$', 'Moderate ($$)'),
        ('$$$', 'Expensive ($$$)'),
        ('$$$$', 'Luxury ($$$$)'),
    ]

    name = models.CharField(max_length=200)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.SET_NULL, null=True, related_name='restaurants')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='restaurants')
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)
    price_range = models.CharField(max_length=10, choices=PRICE_CHOICES, default='$$')
    opening_time = models.TimeField(default=time(9, 0))
    closing_time = models.TimeField(default=time(23, 0))
    image = models.CharField(max_length=500, help_text="Image URL or relative static path")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating', 'name']

    def __str__(self):
        return self.name

    def is_open_now(self):
        now_time = datetime.now().time()
        if self.opening_time <= self.closing_time:
            return self.opening_time <= now_time <= self.closing_time
        else:
            # Handles overnight schedules e.g., 6 PM to 2 AM
            return now_time >= self.opening_time or now_time <= self.closing_time

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Search Histories"

    def __str__(self):
        return f"{self.user.username}: {self.query}"
