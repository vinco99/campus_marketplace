from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('dispatch', 'Dispatch'),
        ('admin', 'Admin')
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

# OTP Number verification
class OTP(models.Model):
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
    
    def __str__(self):
        return f"{self.phone} - {self.code}"


# Dispatch ID verification
class RiderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_card = models.ImageField(upload_to='riders/')
    license = models.ImageField(upload_to='riders/')
    is_approved = models.BooleanField(default=False)