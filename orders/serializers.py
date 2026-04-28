from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'delivery_type', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        # Assume all products from same seller (MVP)
        first_product = items_data[0]['product']
        seller = first_product.seller

        total_price = 0

        order = Order.objects.create(
            buyer=user,
            seller=seller,
            delivery_type=validated_data['delivery_type'],
            total_price=0
        )

        for item in items_data:
            product = item['product']
            quantity = item['quantity']

            price = product.price * quantity
            total_price += price

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

        order.total_price = total_price
        order.save()

        return order
