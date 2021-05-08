import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room


class ChatConsumer(AsyncWebsocketConsumer):
    """Chat with managers accomodation facylity"""

    async def connect(self):
        self.room_name = 'manager'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            })

    @sync_to_async
    def get_room_by_filter(self, number):
        return list(Room.objects.filter(number=number))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Получаем "Забронировать #<номер_комнаты>"
        if message.startswith("Забронировать #"):
            req = message.split("#")
            count = 0
            hotels = set()
            for room in await self.get_room_by_filter(int(req[1])):
                if not room.booking:
                    count += 1
            if count:
                message = "Есть {} не забронированный(ых) номер(ов)".format(count)
            else:
                message = "К сожалению, все номера забронированны"
        else:
            message = "НЕ корректный запрос. Введите: Забронировать №номер"
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
