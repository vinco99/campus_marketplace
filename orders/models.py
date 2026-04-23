from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
    ]

    DELIVERY_TYPE = [
        ('delivery', 'Delivery'),
        ('meetup', 'Meetup'),
    ]

    buyer = models.ForeignKey(User, related_name='buyer_orders', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='seller_orders', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"