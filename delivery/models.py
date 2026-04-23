from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Delivery(models.Model):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE)
    rider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50)