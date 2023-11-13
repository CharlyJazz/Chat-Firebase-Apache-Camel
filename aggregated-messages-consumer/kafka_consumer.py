from kafka import KafkaConsumer
from firebase_admin import credentials, firestore
from typing import Any, Dict

import json
import logging
import firebase_admin
import os

BOOTSTRAP_SERVER_ADDRESS = os.getenv("BOOTSTRAP_SERVER_ADDRESS", "kafka:9092")
CONTAINER_MODE = os.getenv("CONTAINER_MODE", "0")

class KafkaMessageConsumer:
    """
    BOOTSTRAP_SERVER_ADDRESS:
    - If this run using docker-compose it should be: kafka:9092 
    - if this run using local machine python it should be: 29092
    - In k8 is kafka-service:9092
    """
    def __init__(self, topic_name: str, group_id: str, firebase_cred_path: str, test_mode=False) -> None:
        self.topic_name = topic_name
        self.group_id = group_id
        self.firebase_cred_path = firebase_cred_path
        self.test_mode = test_mode
        self.consumer = KafkaConsumer(
            self.topic_name,
            bootstrap_servers=BOOTSTRAP_SERVER_ADDRESS,
            auto_offset_reset='latest',
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        self.initialize_firebase()

    def close(self):
        logging.info("Pausing Consumer")
        self.consumer.pause()
        logging.info("Unsubscribing Consumer")
        self.consumer.unsubscribe()
        logging.info("Closing Consumer")
        self.consumer.close()
        login.info("Consumer turned off successfully")

    def initialize_firebase(self) -> None:
        cred = credentials.Certificate(self.firebase_cred_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.chat_ref = self.db.collection(u'messages')

    def log_message(self, message: Any) -> None:
        logging.info(f" \
GROUP_ID: {self.group_id} \
TOPIC_NAME: {self.topic_name} \
MESSAGE_KEY: {message.key} \
MESSAGE_VALUE: {message.value}"
        )

    def consume_messages(self) -> None:
        logging.info("Starting messages consuming to send to Firestore")
        for message in self.consumer:
            self.log_message(message)
            self.chat_ref.add(message.value)
            if self.test_mode:
                self.close()
