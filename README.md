# Distributed-Logging-System
This project implements a distributed logging and heartbeat monitoring system designed to track and analyze logs from microservice-based applications. By integrating various tools such as Fluentd, Kafka, Elasticsearch, and custom Python scripts, the system provides real-time log aggregation, health monitoring, and alerting functionalities to ensure smooth operations in a microservices architecture.

## Key Features
**Centralized Logging:** Efficiently collects logs from distributed microservices.
**Heartbeat Monitoring:** Tracks the health status of microservice nodes in real-time.
**Alerting Mechanism:** Triggers alerts for critical issues, such as service failures or errors.
**Scalable and Decoupled Architecture:** Utilizes Kafka to decouple log producers and consumers, enabling scalability.
## Architecture Overview
The system is composed of the following key components:

- **Node Simulation (node.py)**
Simulates microservices that generate logs and heartbeat signals periodically.
Sends both heartbeats and logs (INFO, WARN, ERROR) to the Fluentd log aggregator.
- **Log Aggregation (fluentd_kafka.conf)**
Fluentd collects and forwards logs to Kafka topics (LOG and HEARTBEAT) for processing.
Configured to buffer and forward logs and heartbeats for efficient consumption.
- **Kafka Pub/Sub Model**
Kafka acts as the central message broker that decouples producers (microservices) from consumers (log monitoring systems, alerting, and storage).
Topics:
HEARTBEAT: Contains health status updates of microservice nodes.
LOG: Contains various log levels (INFO, WARN, ERROR) generated by the services.
- **Log & Heartbeat Consumers**
Heartbeat Monitoring (heartbeat-monitor.py): Consumes heartbeat messages to track node health. If a node fails to send a heartbeat within a timeout, it triggers an alert.
Log Storage (log-storage.py): Stores and indexes logs into Elasticsearch for querying and analysis. It ensures data integrity by indexing logs into distinct Elasticsearch indexes.
Alerting System (logs-alertsystem.py): Monitors logs for WARN or ERROR levels and triggers alerts when critical issues are detected.
## Workflow
- **Node Generation**
Microservice nodes (simulated via node.py) generate periodic heartbeat messages and logs.
- **Log Aggregation**
Fluentd collects logs and heartbeats and forwards them to Kafka, separating the data into appropriate topics for consumption.
- **Kafka Message Bus**
Kafka decouples the microservices producing logs and heartbeats from the consumers that process and store this data.
- **Health Monitoring**
The heartbeat-monitor.py script monitors node health by checking the time difference between received heartbeat messages. Alerts are raised if a node's heartbeat is overdue.
- **Log Storage**
The log-storage.py script indexes the logs in Elasticsearch, making them available for querying and analysis. Logs are categorized into different indexes based on their nature.
- **Alerting**
The logs-alertsystem.py script checks for WARN and ERROR logs in the Kafka stream and raises alerts for immediate attention.
