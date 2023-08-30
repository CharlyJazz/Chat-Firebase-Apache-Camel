from kafka import KafkaConsumer
import json
import logging
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Any, Dict

class KafkaMessageConsumer:
    def __init__(self, topic_name: str, group_id: str, firebase_cred_path: str, test_mode=False) -> None:
        self.topic_name = topic_name
        self.group_id = group_id
        self.firebase_cred_path = firebase_cred_path
        self.test_mode = test_mode
        self.consumer = KafkaConsumer(
            self.topic_name,
            auto_offset_reset='latest',
            group_id=self.group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        logging.basicConfig(
            level=logging.INFO,
            filename='consumer.log',
            filemode='w',
            format='%(name)s - %(levelname)s - %(message)s'
        )
        self.initialize_firebase()

    def close(self):
        self.consumer.pause()
        self.consumer.unsubscribe()
        self.consumer.close()

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
        for message in self.consumer:
            self.log_message(message)
            self.chat_ref.add(message.value)
            if self.test_mode:
                self.close()
