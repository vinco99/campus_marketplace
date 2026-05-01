from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, InitializePaymentView, VerifyPaymentView, ConfirmDeliveryView

router = DefaultRouter()
router.register('', OrderViewSet, basename='order')

urlpatterns = router.urls
urlpatterns += [
    path('pay/<int:order_id>/', InitializePaymentView.as_view()),
    path('verify-payment/<str:reference>/', VerifyPaymentView.as_view()),
     path('confirm-delivery/<int:order_id>/', ConfirmDeliveryView.as_view()),
]