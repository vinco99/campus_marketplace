from .views import SendOTPView, VerifyOTPView
from django.urls import path

urlpatterns = [
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
]