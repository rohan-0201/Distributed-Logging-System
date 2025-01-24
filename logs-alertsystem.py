from kafka import KafkaConsumer
import json

log_consumer = KafkaConsumer(
    'LOG', #subscribed to LOG topic
    group_id='alert_system',
    enable_auto_commit=True,
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in log_consumer:
	log = message.value
	log_level = log.get('log_level') 
	node_id = log.get('node_id') 
	if log_level=='WARN' or log_level=='ERROR':
		print(f"ALERT: {log_level} log detected at node {node_id}!")
		#print(json.dumps(log, indent=4))  


# Example steps to run the system:
# 1. Start Fluentd: `fluentd -c /home/pes2ug22cs453/Desktop/bdprojrjr/fluentd.conf`
# 2. Run node.py to generate logs: `python3 node.py --node_id 1 --service_name "PaymentService"` (can run more nodes too in diff terminal)
# 3. Run the consumer script: `python3 logs-alertsystem.py`
