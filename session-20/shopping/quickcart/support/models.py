import uuid
from django.db import models
from django.contrib.auth.models import User

class SupportTicket(models.Model):
    CATEGORY_CHOICES = (
        ('Order Issue', 'Order Issue'),
        ('Payment Issue', 'Payment Issue'),
        ('Return & Refund', 'Return & Refund'),
        ('Account & Login', 'Account & Login'),
        ('Coupon / Offer', 'Coupon / Offer'),
        ('Other', 'Other Query'),
    )

    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    )

    ticket_id = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = f"TCK-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.subject} ({self.status})"


class FAQ(models.Model):
    CATEGORY_CHOICES = (
        ('Account', 'Account & Registration'),
        ('Orders', 'Orders & Shipping'),
        ('Payments', 'Payments & Checkout'),
        ('Returns', 'Returns & Refunds'),
        ('Delivery', 'Delivery & Tracking'),
        ('Coupons', 'Coupons & Discounts'),
    )

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return f"[{self.category}] {self.question}"
