from kafka import KafkaClient, errors
from kafka_consumer import KafkaMessageConsumer, BOOSTRAP_SERVER
import json
import logging
import firebase_admin
from firebase_admin import credentials, firestore
import time

def check_kafka_availability(timeout_seconds=120):
    start_time = time.time()
    
    while time.time() - start_time < timeout_seconds:
        try:
            client = KafkaClient(bootstrap_servers=BOOSTRAP_SERVER)
            logging.warning("Kafka Client Successfully Connected")
            client.close()
            return True
        except errors.NoBrokersAvailable:
            logging.warning("Kafka Client Error: errors.NoBrokersAvailable")
            pass  # Continue checking
        
        time.sleep(1)  # Sleep for 1 second before checking again
    
    return False

def main():
    if check_kafka_availability():
        TOPIC_NAME = 'chat_messages_grouped'
        GROUP_ID = 'aggregated-messages-group'
        FIREBASE_CRED_PATH = 'service_account_key.json'
        
        kafka_consumer = KafkaMessageConsumer(
            topic_name=TOPIC_NAME,
            group_id=GROUP_ID,
            firebase_cred_path=FIREBASE_CRED_PATH
        )
        
        kafka_consumer.consume_messages()
    else:
        logging.warning("Kafka is not available. Exiting.")

if __name__ == "__main__":
    main()
