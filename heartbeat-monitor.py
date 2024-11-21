from kafka import KafkaConsumer
import json
import time
from threading import Thread
from datetime import datetime

consumer = KafkaConsumer(
    'HEARTBEAT',  #subscribed to HEARTBEAT topic
    group_id='alert_system',
    enable_auto_commit=True,
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

HEARTBEAT_TIMEOUT = 10 
ALERT_CHECK_INTERVAL = 5 

heartbeat_tracker = {}

def monitor_heartbeats():
    while True:
        current_time = time.time()
        for node_id, last_heartbeat in list(heartbeat_tracker.items()):
            if current_time - last_heartbeat > HEARTBEAT_TIMEOUT:
                print(f"[ALERT] Node '{node_id}' is down! Last heartbeat at {datetime.fromtimestamp(last_heartbeat).strftime('%Y-%m-%d %H:%M:%S')}.")
                del heartbeat_tracker[node_id] 
        time.sleep(ALERT_CHECK_INTERVAL)

Thread(target=monitor_heartbeats, daemon=True).start()

for msg in consumer:
    heartbeat = msg.value
    node_id = heartbeat.get("node_id")
    timestamp = time.time()
    formatted_timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    heartbeat_tracker[node_id] = timestamp
    print(f"[HEARTBEAT] received from Node '{node_id}' at {formatted_timestamp}")
