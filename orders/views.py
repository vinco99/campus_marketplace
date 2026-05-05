import requests
import uuid
from django.conf import settings
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order, Payment
from wallet.models import Wallet, Transaction


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
        
        if hasattr(order, 'payment') and order.payment.verified:
            return Response({"error": "Order already paid"}, status=400)
        

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
    permission_classes = [AllowAny]
    
    def get(self, request, reference):

        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

        response = requests.get(url, headers=headers)
        res_data = response.json()

        if res_data['data']['status'] != 'success':
            return Response({"error": "Payment not successful"}, status=400)

        try:
            payment = Payment.objects.select_related('order').get(reference=reference)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if payment.verified:
            return Response({"message": "Payment already verified"})

        order = payment.order

        with transaction.atomic():
            payment.gateway_response = str(res_data)
            payment.verified = True
            payment.save()

            order_items = order.items.select_related('product').all()
            for item in order_items:
                product = item.product
                product.stock = product.stock - item.quantity
                product.save()

            order.is_paid = True
            order.status = 'paid'
            order.save()

        return Response({"message": "Payment verified successfully"})


class AssignDispatchView(APIView):
    def post(self, request, order_id):
        order = Order.objects.get(id=order_id)

        dispatch = request.user

        if dispatch.role != "dispatch":
            return Response({"error": "Only dispatch can accept delivery"}, status=403)

        order.dispatch = dispatch
        order.status = "processing"
        order.save()

        return Response({"message": "Order assigned"})


class MarkShippedView(APIView):
    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, dispatch=request.user)

        order.status = "shipped"
        order.save()

        return Response({"message": "Order shipped"})


class MarkDeliveredView(APIView):
    def post(self, request, order_id):
        order = Order.objects.get(id=order_id, dispatch=request.user)

        order.status = "delivered"
        order.is_delivered = True
        order.save()

        return Response({"message": "Marked as delivered"}) 


class ConfirmDeliveryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        user = request.user

        try:
            order = Order.objects.get(id=order_id, buyer=user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if order.status != 'delivered':
            return Response({"error": "Order not delivered yet"}, status=400)

        if not order.is_paid:
            return Response({"error": "Order not paid"}, status=400)

        # CREDIT SELLER WALLET
        wallet = Wallet.objects.get(user=order.seller)
        wallet.balance += order.total_price
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            amount=order.total_price,
            type='credit',
            reference=f"order_{order.id}"
        )

        order.status = 'completed'
        order.save()

        return Response({"message": "Order completed & seller credited"})