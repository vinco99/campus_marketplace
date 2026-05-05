import requests
from django.db import transaction
from .models import Transaction
from django.conf import settings

def send_paystack_transfer(withdrawal):
    url = "https://api.paystack.co/transfer"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "source": "balance",
        "amount": int(withdrawal.amount * 100),
        "recipient": withdrawal.recipient_code,  # better design
        "reason": f"Withdrawal {withdrawal.id}"
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()


def process_withdrawal(withdrawal):
    if withdrawal.status == 'paid':
        return {"error": "Already processed"}

    response = send_paystack_transfer(withdrawal)

    if not response.get('status'):
        return {"error": "Transfer failed"}

    if response['data']['status'] != 'success':
        return {"error": "Transfer not successful"}

    wallet = withdrawal.user.wallet

    with transaction.atomic():
        wallet.balance -= withdrawal.amount
        wallet.save()

        Transaction.objects.create(
            wallet=wallet,
            amount=withdrawal.amount,
            type='debit',
            reference=response['data']['reference']
        )

        withdrawal.status = 'paid'
        withdrawal.reference = response['data']['reference']
        withdrawal.save()

    return {"message": "Withdrawal successful"}