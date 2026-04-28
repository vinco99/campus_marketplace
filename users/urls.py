#from .views import SendOTPView, VerifyOTPView
from django.urls import path
from .views import RegisterView, CustomLoginView, SendOTPView, VerifyOTPView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', CustomLoginView.as_view()),
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    #path('refresh/', TokenRefreshView.as_view()),
]
