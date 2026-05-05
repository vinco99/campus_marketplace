from django.urls import path
from .views import WalletView, RequestWithdrawalView

urlpatterns = [
    path('', WalletView.as_view()),
    path('withdraw/', RequestWithdrawalView.as_view()),
]