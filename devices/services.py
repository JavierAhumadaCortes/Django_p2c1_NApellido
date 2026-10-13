import json

from django.conf import settings

def cargar_dispositivos():
    ruta = settings.BASE_DIR / "data" / "dispositivos.json"
    with ruta.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)
    if not isinstance(datos, list):
        raise ValueError("Se esperaba una lista de dispositivos")
    return datos


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def publish_device_status(device):
    channel_layer = get_channel_layer()

    if channel_layer is None:
        return

    async_to_sync(channel_layer.group_send)(
        "ecoenergy_dashboard",
        {
            "type": "device_event",
            "payload": {
                "type": "device_status_changed",
                "device_id": device.id,
                "name": device.name
            },
        },
    )