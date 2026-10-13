# realtime/consumers.py

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DashboardConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(
            "ecoenergy_dashboard",
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "ecoenergy_dashboard",
            self.channel_name,
        )

    async def device_event(self, event):
        await self.send_json(event["payload"])