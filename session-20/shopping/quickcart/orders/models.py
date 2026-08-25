import uuid
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from accounts.models import Address

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('Placed', 'Placed'),
        ('Confirmed', 'Confirmed'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
        ('Refunded', 'Refunded'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Successful', 'Successful'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    )

    order_id = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='orders')
    address_snapshot = models.TextField(help_text="Snapshot of address at time of order")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Placed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"QC-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def can_cancel(self):
        return self.order_status in ['Placed', 'Confirmed', 'Packed']

    def can_return(self):
        return self.order_status == 'Delivered' and not hasattr(self, 'return_request')

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def item_total(self):
        return self.final_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in {self.order.order_id}"


class ReturnRequest(models.Model):
    RETURN_REASON_CHOICES = (
        ('Defective', 'Defective / Damaged Item'),
        ('Wrong Item', 'Received Wrong Item'),
        ('Size Issue', 'Size / Fit Issue'),
        ('Quality Not Expected', 'Quality Not as Expected'),
        ('Mind Changed', 'Changed Mind / No Longer Needed'),
    )

    RETURN_STATUS_CHOICES = (
        ('Requested', 'Requested'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Picked Up', 'Picked Up'),
        ('Refunded', 'Refunded'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='return_request')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='return_requests', null=True, blank=True)
    reason = models.CharField(max_length=50, choices=RETURN_REASON_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=RETURN_STATUS_CHOICES, default='Requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return Request for {self.order.order_id} ({self.status})"
