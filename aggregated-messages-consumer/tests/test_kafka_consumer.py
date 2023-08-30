import pytest
import json
import threading
import time

from firebase_admin import firestore
from kafka import KafkaProducer
from kafka_consumer import KafkaMessageConsumer
from datetime import datetime

@pytest.fixture(scope='module')
def kafka_producer():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    yield producer
    producer.close()

TOPIC_NAME = 'chat_messages_grouped'

@pytest.fixture(scope='module')
def kafka_consumer():
    GROUP_ID = 'test-consumer-group'
    FIREBASE_CRED_PATH = 'service_account_key.json'

    consumer = KafkaMessageConsumer(
        topic_name=TOPIC_NAME,
        group_id=GROUP_ID,
        firebase_cred_path=FIREBASE_CRED_PATH,
        test_mode=True
    )
    yield consumer

def test_integration(kafka_producer, kafka_consumer):
    MESSAGE = {
        "from_user": "charlyjazz",
        "chat_id": "1",
        "time_iso": str(datetime.today()),
        "list_of_messages": [
            {
                "body": "Hello",
                "message_id": "1",
                "chat_id": "1",
                "time": "uuid",
                "time_iso": str(datetime.today()),
                "to_user": "Pepito"
            },
            {
                "body": "How are your mom?",
                "message_id": "3",
                "chat_id": "1",
                "time": "uuid",
                "time_iso": str(datetime.today()),
                "to_user": "Pepito"
            },
            {
                "body": "Wow",
                "message_id": "3",
                "chat_id": "1",
                "time": "uuid",
                "time_iso": str(datetime.today()),
                "to_user": "Pepito"
            }
        ]
    }

    kafka_consumer_thread = threading.Thread(target=kafka_consumer.consume_messages)
    kafka_consumer_thread.start()

    time.sleep(20)

    kafka_consumer_thread.join(timeout=0)

    kafka_producer.send(TOPIC_NAME, json.dumps(MESSAGE).encode('utf-8'))
    kafka_producer.flush()

    time.sleep(20)

    query = kafka_consumer.db.collection(u'messages').where('time_iso', '==', MESSAGE['time_iso']).limit(1).get()
    assert len(query) == 1

    # Get the data from the query result
    stored_message = query[0].to_dict()

    # Ensure that the consumed message matches the stored message
    assert stored_message == MESSAGE
    assert kafka_consumer_thread.is_alive() == False
