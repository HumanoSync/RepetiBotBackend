from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel

from security.api.rest.auth_controller import router as AuthController
from security.api.rest.user_controller import router as UserController

from device.api.rest.robot_controller import router as RobotController
from device.api.rest.movement_controller import router as MovementController
from device.api.rest.position_controller import router as PositionController

from shared.container import Container
from shared.default_data import defaultData
from shared.database import engine
from shared.mqtt_client import mqttClient

container = Container()
robotService = container.robotService()
userRepository = container.userRepository()

# Configuración de callbacks para MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
        mqttClient.subscribe("robot/+/access/status")
        mqttClient.subscribe("robot/+/access/movement")
    else:
        print(f"Conexión fallida. Código de retorno: {rc}")

def on_message(client, userdata, msg):
    topicParts = msg.topic.split('/')
    robotToken = topicParts[1]

    if msg.topic.endswith("/status"):
        if msg.payload.decode() == "disconnected":
            print(f"Robot {robotToken} se ha desconectado")
            robotService.updateConnectionStatus(robotToken, False)
        elif msg.payload.decode() == "connected":
            print(f"Robot {robotToken} se ha conectado")
            robotService.updateConnectionStatus(robotToken, True)
    elif msg.topic.endswith("/movement"):
        # Aquí podrías manejar las respuestas de los movimientos si es necesario
        print(f"Movimiento recibido del robot {robotToken}: {msg.payload.decode()}")

def on_disconnect(client, userdata, rc):
    print("Desconectado del broker MQTT")

# Lifespan handler para manejar el ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar tablas de la base de datos
    SQLModel.metadata.create_all(engine)
    defaultData(userRepository)
    # Configurar el contenedor para la inyección de dependencias
    container.wire(modules=[
        "security.api.rest.auth_controller",
        "security.api.rest.user_controller",
        "device.api.rest.robot_controller",
        "device.api.rest.movement_controller",
        "device.api.rest.position_controller"
    ])

    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.on_disconnect = on_disconnect
    mqttClient.loop_start()
    # Yield permite que la aplicación ejecute normalmente después de que el contexto se ha configurado
    yield

    # Cuando la aplicación se cierra, paramos el loop de MQTT
    mqttClient.loop_stop()
    mqttClient.disconnect()

# Crear la aplicación FastAPI utilizando el lifespan handler
app = FastAPI(lifespan=lifespan)

app.include_router(AuthController)
app.include_router(UserController)

app.include_router(RobotController)
app.include_router(MovementController)
app.include_router(PositionController)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

