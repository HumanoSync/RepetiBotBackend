import asyncio
import websockets

class VideoControlService:
    def __init__(self):
        self.clients = {}  # Diccionario para gestionar clientes por robot_id

    async def register(self, websocket, robotId):
        if robotId not in self.clients:
            self.clients[robotId] = set()
        self.clients[robotId].add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.clients[robotId].remove(websocket)
            if not self.clients[robotId]:
                del self.clients[robotId]

    async def handleIncomingVideo(self, websocket, path):
        robotId = path.split('/')[-1]  # Suponiendo que robotId está en el path
        async for message in websocket:
            if isinstance(message, bytes):
                if robotId in self.clients:
                    await asyncio.gather(*(client.send(message) for client in self.clients[robotId]))
            else:
                print("Recibido mensaje no válido para video")