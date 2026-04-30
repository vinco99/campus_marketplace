from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, InitializePaymentView, VerifyPaymentView

router = DefaultRouter()
router.register('', OrderViewSet, basename='order')

urlpatterns = router.urls
urlpatterns += [
    path('pay/<int:order_id>/', InitializePaymentView.as_view()),
    path('verify-payment/', VerifyPaymentView.as_view()),
]