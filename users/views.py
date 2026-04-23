from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import OTP
from .utils import generate_otp, send_otp

# Create your views here.
class SendOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')

        code = generate_otp()

        OTP.objects.create(phone=phone, code=code)

        send_otp(phone, code)

        return Response({"message": "OTP sent"})

class VerifyOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')

        try:
            otp = OTP.objects.filter(phone=phone).latest('created_at')
        except OTP.DoesNotExist:
            return Response({"error": "OTP not found"}, status=400)

        if otp.is_expired():
            return Response({"error": "OTP expired"}, status=400)

        if otp.code != code:
            return Response({"error": "Invalid OTP"}, status=400)

        user = User.objects.get(phone=phone)
        user.is_phone_verified = True
        user.save()

        return Response({"message": "Phone verified successfully"})