from kafka import KafkaConsumer
from kafka_consumer import KafkaMessageConsumer
import json
import logging
import firebase_admin
from firebase_admin import credentials, firestore

def main():
    TOPIC_NAME = 'chat_messages_grouped'
    GROUP_ID = 'aggregated-messages-group'
    FIREBASE_CRED_PATH = 'service_account_key.json'
    
    kafka_consumer = KafkaMessageConsumer(
        topic_name=TOPIC_NAME,
        group_id=GROUP_ID,
        firebase_cred_path=FIREBASE_CRED_PATH
    )
    
    kafka_consumer.consume_messages()

if __name__ == "__main__":
    main()
