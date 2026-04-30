import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Order, Payment
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
import uuid

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(buyer=user)

    def perform_create(self, serializer):
        serializer.save()


class InitializePaymentView(APIView):
    def post(self, request, order_id):
        user = request.user

        try:
            order = Order.objects.get(id=order_id, buyer=user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        reference = str(uuid.uuid4())

        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": user.email,
            "amount": int(order.total_price * 100),  # kobo
            "reference": reference,
            "callback_url": "http://localhost:8000/api/orders/verify-payment/"
        }

        response = requests.post(url, json=data, headers=headers)
        res_data = response.json()

        Payment.objects.create(
            order=order,
            reference=reference,
            amount=order.total_price
        )

        return Response({
            "payment_url": res_data['data']['authorization_url'],
            "reference": reference
        })


class VerifyPaymentView(APIView):
    def get(self, request):
        reference = request.GET.get('reference')

        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

        response = requests.get(url, headers=headers)
        res_data = response.json()

        if res_data['data']['status'] != 'success':
            return Response({"error": "Payment not successful"}, status=400)

        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        payment.verified = True
        payment.save()

        order = payment.order
        order.is_paid = True
        order.status = 'paid'
        order.save()

        return Response({"message": "Payment verified successfully"})
