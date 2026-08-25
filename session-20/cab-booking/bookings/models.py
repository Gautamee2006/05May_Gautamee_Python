import uuid
from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_CONFIRMED = 'Confirmed'
    STATUS_DRIVER_ASSIGNED = 'Driver Assigned'
    STATUS_ON_THE_WAY = 'On the Way'
    STATUS_COMPLETED = 'Completed'
    STATUS_CANCELLED = 'Cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_DRIVER_ASSIGNED, 'Driver Assigned'),
        (STATUS_ON_THE_WAY, 'On the Way'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    CAB_MINI = 'Mini'
    CAB_SEDAN = 'Sedan'
    CAB_SUV = 'SUV'

    CAB_CHOICES = [
        (CAB_MINI, 'Mini (₹10/km, 3 seats)'),
        (CAB_SEDAN, 'Sedan (₹15/km, 4 seats)'),
        (CAB_SUV, 'SUV (₹20/km, 6 seats)'),
    ]

    PAYMENT_CASH = 'Cash'
    PAYMENT_UPI = 'UPI'
    PAYMENT_CARD = 'Card'

    PAYMENT_CHOICES = [
        (PAYMENT_CASH, 'Cash'),
        (PAYMENT_UPI, 'UPI Payment'),
        (PAYMENT_CARD, 'Debit/Credit Card'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    
    # Pickup info
    pickup_address = models.TextField()
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    
    # Drop info
    drop_address = models.TextField()
    drop_latitude = models.FloatField()
    drop_longitude = models.FloatField()
    
    # Trip calculation metrics
    distance_km = models.FloatField()
    estimated_time = models.CharField(max_length=50, default='15 min')
    
    # Cab & Pricing
    cab_type = models.CharField(max_length=20, choices=CAB_CHOICES, default=CAB_SEDAN)
    base_fare = models.DecimalField(max_digits=8, decimal_places=2, default=50.00)
    per_km_rate = models.DecimalField(max_digits=8, decimal_places=2, default=15.00)
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default=PAYMENT_CASH)
    
    # Status
    booking_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_CONFIRMED)
    
    # Assigned Driver Information (Simulated)
    driver_name = models.CharField(max_length=100, default='Rahul Patel')
    driver_vehicle = models.CharField(max_length=100, default='Swift Dzire')
    driver_number = models.CharField(max_length=20, default='GJ03AB1234')
    driver_phone = models.CharField(max_length=20, default='+91 98765 43210')
    driver_rating = models.FloatField(default=4.8)
    
    user_rating = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_id:
            # Generate unique booking ID e.g. CAB-7X9A2B
            self.booking_id = f"CAB-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_id} - {self.cab_type} ({self.booking_status})"

    @property
    def is_cancellable(self):
        return self.booking_status not in [self.STATUS_COMPLETED, self.STATUS_CANCELLED]
