import uuid
import random
import time
import argparse
import requests

# Fluentd configuration
FLUENTD_URL = "http://localhost:9880/logs"

# Generate a random log
def generate_log(node_id, service_name):
    log_levels = ["INFO", "WARN", "ERROR"]
    log_level = random.choice(log_levels)
    log_id = str(uuid.uuid4())
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    if log_level == "INFO":
        log = {
            "log_id": log_id,
            "node_id": node_id,
            "log_level": log_level,
            "message_type": "LOG",
            "message": "This is an informational log",
            "service_name": service_name,
            "timestamp": timestamp,
        }
    elif log_level == "WARN":
        log = {
            "log_id": log_id,
            "node_id": node_id,
            "log_level": log_level,
            "message_type": "LOG",
            "message": "This is a warning log",
            "service_name": service_name,
            "response_time_ms": random.randint(100, 500),
            "threshold_limit_ms": 200,
            "timestamp": timestamp,
        }
    elif log_level == "ERROR":
        log = {
            "log_id": log_id,
            "node_id": node_id,
            "log_level": log_level,
            "message_type": "LOG",
            "message": "This is an error log",
            "service_name": service_name,
            "error_details": {
                "error_code": random.randint(1000, 5000),
                "error_message": "An error occurred",
            },
            "timestamp": timestamp,
        }
    return log


# Send heartbeat
def send_heartbeat(node_id, status="UP"):
    heartbeat = {
        "node_id": node_id,
        "message_type": "HEARTBEAT",
        "status": status,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return heartbeat


# Send data to Fluentd
def send_log_to_fluentd(log):
    try:
        requests.post(FLUENTD_URL, json=log)
    except requests.RequestException as e:
        print(f"Failed to send log to Fluentd: {e}")


# Main process
def main(node_id, service_name):
    print(f"Node {node_id} ({service_name}) started.")

    # Node registration (via Fluentd)
    reg_msg = {
        "node_id": node_id,
        "message_type": "REGISTRATION",
        "service_name": service_name,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    send_log_to_fluentd(reg_msg)

    while True:
        heartbeat = send_heartbeat(node_id)
        send_log_to_fluentd(heartbeat)  
        time.sleep(5)  # Heartbeat every 5 seconds

        log = generate_log(node_id, service_name)
        send_log_to_fluentd(log)  
        time.sleep(random.randint(1, 3))  # Random log interval


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a microservice node.")
    parser.add_argument(
        "--node_id", type=str, help="Unique Node ID", default=str(uuid.uuid4())
    )
    parser.add_argument("--service_name", type=str, help="Service Name", required=True)
    args = parser.parse_args()

    main(args.node_id, args.service_name)

