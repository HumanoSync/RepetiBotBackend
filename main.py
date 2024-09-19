import asyncio
from websocket_handler import WebSocketHandler
import websockets

async def startDataServer():
    websocketHandler = WebSocketHandler()
    startServer = websockets.serve(websocketHandler.handleMessage, '0.0.0.0', 8765, max_size=None)
    await startServer
    print("Servidor WebSocket JSON-RPC iniciado en el puerto 8765")
    await asyncio.Future()  # Run forever

async def main():
    await startDataServer()

if __name__ == "__main__":
    asyncio.run(main())
