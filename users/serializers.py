from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from .utils import generate_otp, send_otp
from .models import OTP
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'role']

    def create(self, validated_data):
        phone = validated_data.get('phone')

        user = User.objects.create_user(**validated_data)
        user.is_phone_verified = False
        user.save()

        #Delete old OTPs
        OTP.objects.filter(phone=phone).delete()

        #crete New OTP
        code = generate_otp()
        OTP.objects.create(phone=phone, code=code)

        #Send OTP
        send_otp(phone, code)


        return user


class CustomLoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_phone_verified:
            raise AuthenticationFailed("Phone number not verified")

        return data