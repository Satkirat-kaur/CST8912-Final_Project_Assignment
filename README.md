# Real-time Monitoring System for Rideau Canal Skateway

## 1. Scenario Description

The Rideau Canal Skateway in Ottawa is one of the most iconic outdoor attractions during winter. To ensure public safety and enhance operational decision-making, a real-time monitoring system is proposed. This system uses simulated IoT sensors installed at key locations—such as **Dow’s Lake**, **Fifth Avenue**, and **Pretoria Bridge** —to collect critical data about ice conditions and weather factors like temperature, humidity, and wind speed.

The data collected is streamed to **Azure IoT Hub**, where it is securely received and forwarded to **Azure Stream Analytics**. Here, real-time rules are applied to detect unsafe skating conditions by analyzing ice thickness and environmental parameters. The processed and filtered data is then stored in **Azure Blob Storage** for historical tracking and further analysis.

This smart solution provides a scalable and reliable architecture to support safe recreational activities and data-driven decision-making for city officials.

> **Note**: The original plan was to simulate the NAC (National Arts Centre) location. However, during implementation, I proceeded with the **Pretoria Bridge** sensor instead. By the time I realized the change, the simulation scripts and setup were already completed. To maintain consistency and meet deadlines, I continued using Pretoria Bridge as the third sensor location.

## 2. System Architecture
![System Architecture Diagram](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/System%20Architecture%20Diagram.png)

This system is built to simulate and process real-time environmental data from the Rideau Canal Skateway. It monitors key factors like ice thickness and weather conditions to help determine safe or unsafe skating conditions. The architecture is composed of four main components:

### 1. **Simulated IoT Devices**
Three virtual sensors are placed at key locations along the canal: **Pretoria Bridge**, **Dow’s Lake**, and **Fifth Avenue**. These sensors continuously generate telemetry data, including:
- Ice thickness
- Air temperature
- Humidity
- Wind speed

Each sensor acts as a data source, simulating real-world input from the field.

### 2. **Azure IoT Hub**
All data from the simulated devices is securely transmitted to **Azure IoT Hub**, which acts as the central communication gateway. It manages:
- Device authentication
- Secure data ingestion
- Routing of telemetry to downstream services

### 3. **Azure Stream Analytics**
Incoming data is then processed in **Azure Stream Analytics**, where two core operations take place:
- **Threshold Analysis:** Checks if any measurements exceed defined safety limits (e.g., low ice thickness).
- **Data Transformation:** Filters, formats, and prepares the data for storage or further analysis.

### 4. **Azure Blob Storage**
Processed results are saved to **Azure Blob Storage**, which provides scalable and secure long-term storage. This allows city officials or analysts to access historical trends, generate reports, or build dashboards using tools like Power BI.

### Diagram Explanation

The architecture diagram visualizes this flow from left to right:

- **Simulated IoT Devices**: Represent sensors that feed real-time data into the system.
- **Azure IoT Hub**: Acts as the message broker between the edge devices and cloud processing.
- **Azure Stream Analytics**: Performs live data analysis and filtering.
- **Azure Blob Storage**: Collects the processed data for storage, reporting, or integration.

This setup ensures a seamless flow from sensor simulation to cloud-based storage, offering a practical and scalable solution for real-time ice condition monitoring.

## 3. Implementation Details

### IoT Sensor Simulation

Three Python scripts were created using the Azure IoT SDK (`azure-iot-device`). Each script simulates one sensor and sends data every 10 seconds in JSON format:

```json
{
  "location": "Dow's Lake",
  "iceThickness": 32,
  "surfaceTemperature": -3,
  "snowAccumulation": 5,
  "externalTemperature": -6,
  "timestamp": "2025-04-14T15:30:00Z"
}
```
The Python scripts — `dows_lake_simulator.py`, `fifth_avenue_simulator.py`, and `pretoria_bridge_simulator.py` — randomly generate realistic sensor values such as ice thickness, temperature, and snow accumulation to simulate real-world environmental data.

### Azure IoT Hub Configuration

- **IoT Hub Name**: `CanalIoTHub`
  ![Azure IoT Hub Configuration](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/CanalIoTHub%20Creation.png)
- Each sensor was registered as an individual **device**:

  - `dows-lake`
    
![Dow's Lake Device Creation](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/dows-lake-device%20creation.png)
  
  - `fifth-avenue`
    
![Fifith-Avenue Device Creation](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/fifth-avenue-device%20creation.png)
  
  - `pretoria-bridge`
    
![Pretoria-Bridge Device Creation](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/pretoria-bridge-device%20creation.png)

- Messages from each device were sent to the built-in IoT Hub endpoint:
  - `messages/events`
> These devices were configured using the Azure Portal and authenticated using their primary connection strings in each Python simulation script.

### Azure Stream Analytics Job

The Azure Stream Analytics job (`canal-analytics`) plays a central role in processing the data coming from the simulated IoT devices in real time.
![Canal Analytic Job Creation](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/stream-canal-analytics-job-creation.png)

![Canal Analytic Job created](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/canal-analytic-ctreated.png)

#### 1. Inputs

The job is connected to the Azure IoT Hub input named `canalinput`, which streams live telemetry data sent by the registered devices:
  - Dow’s Lake
  - Fifth Avenue
  - Pretoria Bridge
    ![Adding Job Input](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/adding%20canal-input.png)

  The input is configured to read from the default built-in endpoint: `messages/events`.

#### 2. Query Logic

To analyze and summarize incoming data, I wrote a SQL-like query that groups incoming messages based on their `location` and applies aggregations over a 5-minute tumbling window.

Here is the query used:

```sql
SELECT  
    location, 
    AVG(iceThickness) AS avgIceThickness,
    MAX(snowAccumulation) AS maxSnowAccumulation,
    MIN(surfaceTemperature) AS minSurfaceTemp,
    MAX(externalTemperature) AS maxExternalTemp,
    COUNT(*) AS totalMessages,
    System.Timestamp AS reportTime
INTO
    canaloutput
FROM
    canalinput
GROUP BY
    location,
    TumblingWindow(minute, 5)
```
![Query Logic](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/canalanalytic_query.png)

This query allows the system to:

-  Calculate average ice thickness per location  
-  Identify the highest snow accumulation in a time window  
-  Capture extreme temperature conditions (min/max)  
-  Count how many messages were received from each sensor  

The result is a clean, time-based summary that’s ideal for **safety evaluation** and **visualization**.

---

#### 3. Outputs

The output of this job (`canaloutput`) is configured to write processed results to an **Azure Blob Storage** container in **JSON format**.  
Each file contains the **aggregated data per location** for each 5-minute window, grouped by sensor.
![outputs](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/canal%20output%20created.png)


### Azure Blob Storage

- **Container Name**: `canaloutputcontainer`
- **Output Path Format**: `data/{date}/{time}.json`
- **File Format**: JSON
- Each file contains **aggregated values** per location, generated every 5-minute window by the Stream Analytics job.

  ![Storage Account created](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/storage%20account%20created.png)

> This Jason file includes average ice thickness, max snow accumulation, and temperature extremes for Dow’s Lake, Fifth Avenue, and Pretoria Bridge.
 ![Container overview](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/outpu%20json%20blob%20window.png)

## 4. Usage Instructions

### Running the IoT Sensor Simulations

#### Step 1: Create a Python virtual environment

```bash
python -m venv venv
```

### Step 2: Activate the Environment

**Windows:**

```bash
.\venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Each Simulator in Its Own Terminal

```bash
python dows_lake_simulator.py
python fifth_avenue_sensor.py
python pretoria_bridge_sensor.py
```
#### 1. python dows_lake_simulator.py
 ![Dow's-lake-script running](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/dows-lake-script-running.png)

#### 2. python fifth_avenue_sensor.py
 ![Fift Avenue-script-running](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/fifth-avenue-script-running.png)

 #### 3. python pretoria_bridge_sensor.py
 ![Pretoria-bridge-script-running](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/pretoria-bridge-script%20running.png)

- Each simulator sends data to the IoT Hub every 10 seconds.
- Run all three scripts simultaneously in separate terminals for full sensor coverage.

## Configuring Azure Services

### IoT Hub

- Register each device manually in the Azure IoT Hub:
  - `dows-lake`
  - `fifth-avenue`
  - `pretoria-bridge`
    ![Azure IoT Hub Device Creation](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/CanalIoTHub%20all%20devices.png)
- Copy the **primary connection string** for each device
- Paste the correct connection string into the corresponding simulator script for:
'''
  device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
'''
### Stream Analytics

- **Input**: `canalinput` connected to the IoT Hub's `messages/events` endpoint
- **Output**: `canaloutput` configured to write to Azure Blob Storage
- After setting up input and output, **start the Stream Analytics job** only **after** the simulator scripts are running
  ![Canal Analytics running status](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/stream-canal-analytics-start%20job.png)

- canal-analytics job process running:
  
   ![Canal analytics job overview](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/canalanalytics_overview.png)

## 5. Result: Accessing Stored Data

1. Open the **Azure Portal** and go to **Storage Accounts**
  ![Storage account](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/storage%20account%20created.png) 
  
2. Navigate to your Blob container:
  
3. Select and download any `.json` file
   ![Download jason file](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/outpu%20json%20blob%20window.png)  
  
4. Open the file locally to view the processed output containing aggregated sensor data
    ![Funal Json output](https://github.com/Satkirat-kaur/CST8912-Final_Project_Assignment/blob/main/Screenshots/Final%20Output.png)  

## Reflection

### Challenges Faced During Implementation

- **Mismatch in planned vs. implemented sensor location**:  
  It was originally said to use **NAC (National Arts Centre)** as one of the sensor points. However, I realized too late that I had used **Pretoria Bridge** in the simulation scripts and Azure device setup. Since the system was functioning correctly and the data was valid, I decided to move forward with Pretoria Bridge. 

- **Fifth Avenue data not appearing initially**:  
  Even though the Fifth Avenue simulator was running, no data appeared in the output at first. After troubleshooting, I realized that **Azure Stream Analytics only processes live data** — it does not pick up messages that were sent before the job started. I fixed this by restarting the simulator **after** the Stream Analytics job was running.

- **Strict field naming in Stream Analytics**:  
  I learned that field names like `location` are **case-sensitive** and must match exactly with what’s referenced in the query. Any mismatch (like `Location` or `LOC`) would prevent the query from recognizing the data.

### Lessons Learned During Implimentation

- The importance of starting the Stream Analytics job **before** running simulators
- Why consistency in JSON formatting and field names is crucial for successful query execution
- How cloud tools like Azure IoT Hub, Stream Analytics, and Blob Storage can work together to build scalable, real-time data processing pipelines

## b. IoT Sensor Simulation Code

- The Python scripts used to simulate the IoT sensors were written in **Visual Studio Code (VS Code)**, as shown previously in this file.
- All simulation scripts are organized under the directory.
- Each script is written using the `azure-iot-device` SDK
- It sends randomized but realistic sensor data every 10 seconds
- Uses a unique device connection string for secure communication with Azure IoT Hub

### Running Instructions:
1. Navigate to the `Sensor-Simulators/` folder
2. Activate your virtual environment
3. Run the script using:
```bash
python <script_name>.py
```
- Each script will begin sending data to IoT Hub and print output in the terminal.
- Scripts are designed to run in parallel — open a new terminal window for each simulator.

