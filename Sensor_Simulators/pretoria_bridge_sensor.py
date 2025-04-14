import random
import json
import time
import datetime
from azure.iot.device import IoTHubDeviceClient, Message

def generate_pretoria_bridge_data():
    return {
        "location": "Pretoria Bridge",
        "iceThickness": random.randint(22, 42),
        "surfaceTemperature": random.randint(-6, 4),
        "snowAccumulation": random.randint(0, 12),
        "externalTemperature": random.randint(-11, -1),
        "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'
    }

# Replace with your Pretoria Bridge device connection string
CONNECTION_STRING = "HostName=CanalIoTHub.azure-devices.net;DeviceId=pretoria-bridge;SharedAccessKey=Ww+u+YfheQLEGhzzkd1bB3tPRcpo6HDdJpKkxodPDeM="
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

try:
    print("🚀 Connecting to Azure IoT Hub for Pretoria Bridge...")
    device_client.connect()

    while True:
        data = generate_pretoria_bridge_data()
        message = Message(json.dumps(data))
        device_client.send_message(message)
        print(f"📤 Sent from Pretoria Bridge: {data}")
        time.sleep(10)

except KeyboardInterrupt:
    print("❌ Pretoria Bridge simulation stopped by user.")

finally:
    device_client.disconnect()
    print("🔌 Disconnected Pretoria Bridge device.")
