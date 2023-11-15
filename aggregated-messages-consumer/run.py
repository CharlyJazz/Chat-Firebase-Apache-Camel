from kafka import KafkaClient, errors
from kafka_consumer import KafkaMessageConsumer, BOOTSTRAP_SERVER_ADDRESS, CONTAINER_MODE

import logging
import json
import os
import sys
import time

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, self.datefmt),
        }

        log_record['environment'] = 'development'
        log_record['service'] = 'aggregated-messages-consumer'

        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_record)


if CONTAINER_MODE == "1":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),  # Ensures logs go to stdout which is what Docker expects
        ]
    )

    # Setting the formatter for the root logger to use the JsonFormatter
    logging.getLogger().handlers[0].setFormatter(JsonFormatter())
elif CONTAINER_MODE == "0":
    logging.basicConfig(
        level=logging.DEBUG,
        filename='consumer.log',
        filemode='w',
        format='%(name)s - %(levelname)s - %(message)s'
    )

logging.info("CONTAINER_MODE = <{}>".format(CONTAINER_MODE))

logging.info("BOOTSTRAP_SERVER_ADDRESS = <{}>".format(BOOTSTRAP_SERVER_ADDRESS))

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
        FIREBASE_CRED_PATH = './firebase/service_account_key.json'

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
