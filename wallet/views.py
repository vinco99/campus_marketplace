from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wallet, Withdrawal
from .serializers import WalletSerializer

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    

class RequestWithdrawalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role != "seller":
            return Response({"error": "Only sellers can withdraw"}, status=403)

        amount = float(request.data.get('amount'))

        wallet = Wallet.objects.get(user=user)

        if wallet.balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        withdrawal = Withdrawal.objects.create(
            user=user,
            amount=amount,
            bank_name=request.data.get('bank_name'),
            account_number=request.data.get('account_number'),
            account_name=request.data.get('account_name'),
        )

        return Response({
            "message": "Withdrawal request created",
            "id": withdrawal.id
        })