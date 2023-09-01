import pytest
import json
import threading
import time

from firebase_admin import firestore
from kafka import KafkaProducer
from kafka_consumer import KafkaMessageConsumer
from datetime import datetime

from kafka import KafkaAdminClient

TEST_ID = "TEST_KAFKA_CONSUMER"
TOPIC_NAME = 'chat_messages_grouped'

MESSAGE = {
    "test_id": TEST_ID,
    "from_user": "charlyjazz",
    "chat_id": "1",
    "time_iso": "N/A",
    "list_of_messages": [
        {
            "body": "Hello",
            "message_id": "1",
            "chat_id": "1",
            "time": "uuid",
            "time_iso": "N/A",
            "to_user": "Pepito"
        },
        {
            "body": "How are your mom?",
            "message_id": "3",
            "chat_id": "1",
            "time": "uuid",
            "time_iso": "N/A",
            "to_user": "Pepito"
        },
        {
            "body": "Wow",
            "message_id": "3",
            "chat_id": "1",
            "time": "uuid",
            "time_iso": "N/A",
            "to_user": "Pepito"
        }
    ]
}

@pytest.fixture(scope='module')
def kafka_producer():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    yield producer
    producer.close()

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

@pytest.fixture(scope='module')
def firestore_query(kafka_consumer):
    return kafka_consumer.db.collection(u'messages').where('test_id', '==', TEST_ID).limit(1).get

def test_integration(kafka_producer, kafka_consumer, firestore_query):
    kafka_producer.send(TOPIC_NAME, json.dumps(MESSAGE).encode('utf-8'))
    kafka_producer.flush()
    kafka_consumer_thread = threading.Thread(target=kafka_consumer.consume_messages)
    kafka_consumer_thread.start()
    kafka_consumer_thread.join(timeout=5)
    query = firestore_query()
    retry_count = 1

    while len(query) == 0:
        print("Waiting {} seconds".format(retry_count))
        time.sleep(retry_count)
        retry_count += retry_count
        query = firestore_query()

    # Get the data from the query result
    stored_message = query[0].to_dict()

    # Ensure that the consumed message matches the stored message
    assert stored_message == MESSAGE
    assert kafka_consumer_thread.is_alive() == False