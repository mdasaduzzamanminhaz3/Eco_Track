from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import ChatMessage
from waste.models import PickupRequest


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pickup_id = self.scope['url_route']['kwargs']['pickup_id']
        self.room_group_name = f'chat_{self.pickup_id}'

        # Join the Redis Channel Group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
    # Leave the Redis Channel Group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # This method will be called when a message arrives from the frontend (websocket)
    # testing purpose
    # async def receive(self, text_data):
    #         data = json.loads(text_data)
    #         message = data['message']
            
    #         # সাময়িকভাবে ইফ কন্ডিশন ছাড়া সরাসরি সেভ ও গ্রুপ সেন্ড করছি
    #         if message.strip():
    #             await self.save_message(message) # এখানে আর user পাস করছি না

    #             await self.channel_layer.group_send(
    #                 self.room_group_name,
    #                 {
    #                     'type': 'chat_message',
    #                     'message': message,
    #                     'sender_email': "test@ecotrack.com",
    #                     'sender_name': "Test User"
    #                 }
    #             )
    async def receive(self,text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope.get("user")

        if user.is_authenticated and message.strip():
            # Saving messages to the database (asynchronously)
            await self.save_message(user, message)
            # Sending the message to the entire chat group (Redis will handle it)
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_email': user.email,
                'sender_name': f"{user.first_name} {user.last_name}".strip() or user.email

            }
            )
    # Receiving messages from groups and pushing them to the frontend
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_email': event['sender_email'],
            'sender_name': event['sender_name']
        }))
    @database_sync_to_async
    def save_message(self,user,message):
        pickup = PickupRequest.objects.get(id=self.pickup_id)
        return ChatMessage.objects.create(
            pickup_request=pickup,
            sender=user,
            message=message
        )
    # test perpose
    # @database_sync_to_async
    # def save_message(self, message):
    #     from django.contrib.auth import get_user_model
    #     User = get_user_model()
        
    #     # ডাটাবেজের একদম প্রথম ইউজারকে sender হিসেবে ধরে নিচ্ছি টেস্টের জন্য
    #     fallback_user = User.objects.first() 
    #     pickup = PickupRequest.objects.get(id=self.pickup_id)
        
    #     return ChatMessage.objects.create(
    #         pickup_request=pickup,
    #         sender=fallback_user, # ফিক্সড ইউজার
    #         message=message
    #     )



