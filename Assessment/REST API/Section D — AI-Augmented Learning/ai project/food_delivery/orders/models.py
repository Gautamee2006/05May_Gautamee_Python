from django.db import models


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} ({self.item} x {self.quantity})"
