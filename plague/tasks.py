# tasks.py

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_prediction_to_websocket(prediction):
    channel_layer = get_channel_layer()
    # Aquí 'plague_updates' debe coincidir con el nombre del canal de WebSocket
    async_to_sync(channel_layer.group_send)(
        'plague_updates',  # Nombre del grupo al que quieres enviar el mensaje
        {
            'type': 'send_prediction',
            'prediction': prediction
        }
    )
