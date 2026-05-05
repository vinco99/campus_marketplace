from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import MessageSerializer, ConversationSerializer
from products.models import Product
from orders.models import Order


class StartConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        buyer = request.user
        seller = product.seller

        conversation = Conversation.objects.filter(
            product=product,
            participants=buyer
        ).first()

        if not conversation:
            conversation = Conversation.objects.create(product=product)
            conversation.participants.add(buyer, seller)

        return Response({"conversation_id": conversation.id})    


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        text = request.data.get("text")

        conversation = Conversation.objects.get(id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response({"error": "Not allowed"}, status=403)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            text=text
        )

        return Response(MessageSerializer(message).data)
    

class GetMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if request.user not in conversation.participants.all():
            return Response({"error": "Not allowed"}, status=403)

        messages = conversation.messages.all().order_by("created_at")
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)
    

class CreateOrderFromChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        quantity = int(request.data.get("quantity"))
        delivery_type = request.data.get("delivery_type")

        conversation = get_object_or_404(Conversation, id=conversation_id)
        product = conversation.product

        order = Order.objects.create(
            buyer=request.user,
            seller=product.seller,
            delivery_type=delivery_type,
            total_price=product.price * quantity
        )

        # create order item (if you have model)
        order.items.create(
            product=product,
            quantity=quantity,
            price=product.price
        )

        conversation.order = order
        conversation.save()

        return Response({"order_id": order.id})