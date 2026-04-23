from django.contrib import admin
from .models import User, RiderProfile, OTP

# Register your models here.
admin.site.register(User)
admin.site.register(RiderProfile)
admin.site.register(OTP)