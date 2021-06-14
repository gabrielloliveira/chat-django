import json
from datetime import datetime, date
from decimal import Decimal

from channels.generic.websocket import AsyncWebsocketConsumer


def serialize_queryset(data):
    for el in data:
        for key, _ in el.items():
            if isinstance(el[key], datetime) or isinstance(el[key], date) or isinstance(el[key], Decimal):
                el[key] = str(el[key])
    return data


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.organization = self.scope['url_route']['kwargs']['organization']
        self.room_group_name = f'organization_{self.organization}'
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

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': text_data_json["type"],
                'data': text_data_json.get("data")
            }
        )

    async def update_helpdesk(self, event):
        await self.send(text_data=json.dumps({
            'type': "update_helpdesk",
            'data': event.get('data'),
        }))

    async def new_message(self, event):
        await self.send(text_data=json.dumps({
            'type': "new_message",
            'data': event.get('data'),
        }))

    async def update_message(self, event):
        await self.send(text_data=json.dumps({
            'type': "update_message",
            'data': event.get('data'),
        }))
