# shared/mqtt_client.py
import os
import paho.mqtt.client as mqtt

MQTT_BROKER_URL = os.getenv("MQTT_BROKER_URL")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID")

mqttClient = mqtt.Client(client_id=MQTT_CLIENT_ID)
mqttClient.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.tls_set()
mqttClient.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, 60)

