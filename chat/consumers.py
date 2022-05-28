import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from account.models import User


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add (
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'tester_message',
        #         'tester': 'Hello 11',
        #     }
        # )
        # def tester_message(self, event):
        #     tester = event['tester']
        #
        #     self.send(text_data=json.dumps({
        #         'tester': tester
        #     }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard (
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send (
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


        # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

