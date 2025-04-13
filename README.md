## Scenario Description

The Rideau Canal Skateway in Ottawa is one of the most iconic outdoor attractions during winter. To ensure public safety and enhance operational decision-making, a real-time monitoring system is proposed. This system uses simulated IoT sensors installed at key locations—such as **Dow’s Lake**, **Fifth Avenue**, and **Pretoria Bridge**—to collect critical data about ice conditions and weather factors like temperature, humidity, and wind speed.

The data collected is streamed to **Azure IoT Hub**, where it is securely received and forwarded to **Azure Stream Analytics**. Here, real-time rules are applied to detect unsafe skating conditions by analyzing ice thickness and environmental parameters. The processed and filtered data is then stored in **Azure Blob Storage** for historical tracking and further analysis.

This smart solution provides a scalable and reliable architecture to support safe recreational activities and data-driven decision-making for city officials.

## System Architecture

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

---

### Diagram Explanation

The architecture diagram visualizes this flow from left to right:

- **Simulated IoT Devices**: Represent sensors that feed real-time data into the system.
- **Azure IoT Hub**: Acts as the message broker between the edge devices and cloud processing.
- **Azure Stream Analytics**: Performs live data analysis and filtering.
- **Azure Blob Storage**: Collects the processed data for storage, reporting, or integration.

This setup ensures a seamless flow from sensor simulation to cloud-based storage, offering a practical and scalable solution for real-time ice condition monitoring.
