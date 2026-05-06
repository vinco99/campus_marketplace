import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from asgiref.sync import sync_to_async

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.conversation_id}"

        user = self.scope["user"]

        # Check if user is participant
        is_allowed = await self.is_participant(user)

        if not is_allowed:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope["user"]

        # Save message
        msg_obj = await self.save_message(user, message)

        # Broadcast message
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.username,
                'timestamp': str(msg_obj.created_at)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))

    @sync_to_async
    def is_participant(self, user):
        try:
            convo = Conversation.objects.get(id=self.conversation_id)
            return user in convo.participants.all()
        except:
            return False

    @sync_to_async
    def save_message(self, user, message):
        convo = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=convo,
            sender=user,
            text=message
        )