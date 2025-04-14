import random
import json
import time
import datetime
from azure.iot.device import IoTHubDeviceClient, Message

def generate_fifth_avenue_data():
    return {
        "location": "Fifth Avenue",
        "iceThickness": random.randint(18, 38),
        "surfaceTemperature": random.randint(-7, 3),
        "snowAccumulation": random.randint(1, 10),
        "externalTemperature": random.randint(-12, -2),
        "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'
    }

# Replace with your Fifth Avenue device connection string
CONNECTION_STRING = "HostName=CanalIoTHub.azure-devices.net;DeviceId=fifth-avenue;SharedAccessKey=Biq6+wUjAmrwyJ4yFIHz6RbaH6I7wENawj+4TxAO/Bo="
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

try:
    print("🚀 Connecting to Azure IoT Hub for Fifth Avenue...")
    device_client.connect()

    while True:
        data = generate_fifth_avenue_data()
        message = Message(json.dumps(data))
        device_client.send_message(message)
        print(f"📤 Sent from Fifth Avenue: {data}")
        time.sleep(10)

except KeyboardInterrupt:
    print("❌ Fifth Avenue simulation stopped by user.")

finally:
    device_client.disconnect()
    print("🔌 Disconnected Fifth Avenue device.")
