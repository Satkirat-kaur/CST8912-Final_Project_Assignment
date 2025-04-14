import random
import json
import time
import datetime
from azure.iot.device import IoTHubDeviceClient, Message

# Function to simulate Dow's Lake sensor data
def generate_dows_lake_data():
    return {
        "location": "Dow's Lake",
        "iceThickness": random.randint(20, 40),         # in cm
        "surfaceTemperature": random.randint(-5, 5),    # in °C
        "snowAccumulation": random.randint(0, 15),      # in cm
        "externalTemperature": random.randint(-10, 0),  # in °C
        "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'
    }

# Replace with your actual device connection string 
CONNECTION_STRING = "HostName=CanalIoTHub.azure-devices.net;DeviceId=dows-lake;SharedAccessKey=IVba9UlsuEO8SchbAE3jZdrn/MgCrudI8Ri7Od/Qu7I="
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

try:
    print("🚀 Connecting to Azure IoT Hub...")
    device_client.connect()
    
    print("📡 Sending simulated data from Dow's Lake every 10 seconds...")
    while True:
        data = generate_dows_lake_data()
        message = Message(json.dumps(data))
        device_client.send_message(message)
        print(f"✅ Sent: {data}")
        time.sleep(10)

except KeyboardInterrupt:
    print("❌ Simulation stopped by user.")

finally:
    device_client.disconnect()
    print("🔌 Disconnected from Azure IoT Hub.")
