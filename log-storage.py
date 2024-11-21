from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

es = Elasticsearch(
    hosts=[{"host": "localhost", "port": 9200, "scheme": "http"}]
)

LOG_INDEX_NAME = "fluentd-logs"
REGISTRY_INDEX_NAME = "node-registry"

if not es.indices.exists(index=LOG_INDEX_NAME):
    es.indices.create(index=LOG_INDEX_NAME)
    print(f"Index '{LOG_INDEX_NAME}' created in Elasticsearch.")

if not es.indices.exists(index=REGISTRY_INDEX_NAME):
    es.indices.create(index=REGISTRY_INDEX_NAME)
    print(f"Index '{REGISTRY_INDEX_NAME}' created in Elasticsearch.")

consumer = KafkaConsumer(
    'LOG',  
    'HEARTBEAT', 
    'REGISTRATION', 
    group_id='log-indexer-group',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest'
)

for message in consumer:
    log_data = message.value  

    if log_data.get("message_type") == "HEARTBEAT":
        print(f"Heartbeat received from node: {log_data['node_id']} with status: {log_data['status']}")

        if "log_id" not in log_data:
            log_data["log_id"] = message.offset

        try:
            es.index(index=LOG_INDEX_NAME, id=log_data["log_id"], document=log_data)
            print(f"Indexed heartbeat {log_data['log_id']} into Elasticsearch.")
        except Exception as e:
            print(f"Failed to index heartbeat: {e}")
    
    elif log_data.get("message_type") == "REGISTRATION":
        print(f"Registration received for node: {log_data['node_id']} with details: {log_data}")

        if "registration_id" not in log_data:
            log_data["registration_id"] = message.offset

        try:
            es.index(index=REGISTRY_INDEX_NAME, id=log_data["registration_id"], document=log_data)
            print(f"Indexed registration {log_data['registration_id']} into Elasticsearch.")
        except Exception as e:
            print(f"Failed to index registration: {e}")
    
    else:
        if "log_id" not in log_data:
            log_data["log_id"] = message.offset

        try:
            es.index(index=LOG_INDEX_NAME, id=log_data["log_id"], document=log_data)
            print(f"Indexed log {log_data['log_id']} into Elasticsearch.")
        except Exception as e:
            print(f"Failed to index log: {e}")
