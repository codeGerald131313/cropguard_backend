# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PlagueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Unirse al grupo de WebSocket
        await self.channel_layer.group_add(
            'plague_updates',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Dejar el grupo de WebSocket
        await self.channel_layer.group_discard(
            'plague_updates',
            self.channel_name
        )

    async def receive(self, text_data):
        pass  # No es necesario manejar la recepción en este caso

    async def send_prediction(self, event):
        # Enviar el mensaje de predicción al WebSocket
        prediction = event['prediction']
        await self.send(text_data=json.dumps({
            'status': 'success',
            'prediction': prediction
        }))
