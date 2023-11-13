from kafka import KafkaClient, errors
from kafka_consumer import KafkaMessageConsumer, BOOTSTRAP_SERVER_ADDRESS, CONTAINER_MODE

import logging
import time
import os

logging.warning("CONTAINER_MODE = <{}>".format(CONTAINER_MODE))

logging.warning("BOOTSTRAP_SERVER_ADDRESS = <{}>".format(BOOTSTRAP_SERVER_ADDRESS))


if CONTAINER_MODE == "1":
    logging.basicConfig(
        level=logging.INFO,
        format='%(name)s - %(levelname)s - %(message)s'
    )
elif CONTAINER_MODE == "0":
    logging.basicConfig(
        level=logging.DEBUG,
        filename='consumer.log',
        filemode='w',
        format='%(name)s - %(levelname)s - %(message)s'
    )


def check_kafka_availability(timeout_seconds=120):
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        try:
            client = KafkaClient(bootstrap_servers=BOOTSTRAP_SERVER_ADDRESS)
            logging.info("Kafka Client Successfully Connected")
            client.close()
            return True
        except errors.NoBrokersAvailable:
            logging.warning("No brokers available, let's wait 1 second to check again")
            pass
        time.sleep(1)

    return False

def main():
    if check_kafka_availability():
        TOPIC_NAME = 'chat_messages_grouped'
        GROUP_ID = 'aggregated-messages-group'
        FIREBASE_CRED_PATH = 'service_account_key.json'

        logging.info("Starting KafkaMessageConsumer initialization TOPIC_NAME: {} GROUP_ID:{} FIREBASE_CRED_PATH:{}".format(TOPIC_NAME, GROUP_ID, FIREBASE_CRED_PATH))

        kafka_consumer = KafkaMessageConsumer(
            topic_name=TOPIC_NAME,
            group_id=GROUP_ID,
            firebase_cred_path=FIREBASE_CRED_PATH
        )
        
        kafka_consumer.consume_messages()
    else:
        logging.error("Kafka is not available therefore we can not use KafkaMessageConsumer. Exiting.")

if __name__ == "__main__":
    main()
