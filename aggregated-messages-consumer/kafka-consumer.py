from kafka import KafkaConsumer
import json
import logging
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase
cred = credentials.Certificate("service_account_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
chat_ref = db.collection(u'messages')
# Logger
logging.basicConfig(
  level=logging.INFO, 
  filename='consumer.log', 
  filemode='w', 
  format='%(name)s - %(levelname)s - %(message)s'
)

TOPIC_NAME = 'chat_messages_grouped'
GROUP_ID = 'aggregated-mesages-group'
consumer = KafkaConsumer(
  TOPIC_NAME,
  auto_offset_reset='latest',
  group_id=GROUP_ID,
  value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

if __name__ == "__main__":
  for message in consumer:
    logging.info(f" \
GROUP_ID: {GROUP_ID} \
TOPIC_NAME: {TOPIC_NAME} \
MESSAGE_KEY: {message.key} \
MESSAGE_VALUE: {message.value}"
    )
    chat_ref.add(message.value)