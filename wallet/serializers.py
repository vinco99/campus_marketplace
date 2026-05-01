from rest_framework import serializers
from .models import Wallet, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, source='transaction_set', read_only=True)

    class Meta:
        model = Wallet
        fields = ['balance', 'transactions']