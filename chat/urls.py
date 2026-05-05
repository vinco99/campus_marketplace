from django.urls import path
from .views import (
    StartConversationView,
    SendMessageView,
    GetMessagesView,
    CreateOrderFromChatView
)

urlpatterns = [
    path('start/', StartConversationView.as_view()),
    path('send/', SendMessageView.as_view()),
    path('<int:conversation_id>/', GetMessagesView.as_view()),
    path('order/', CreateOrderFromChatView.as_view()),
]