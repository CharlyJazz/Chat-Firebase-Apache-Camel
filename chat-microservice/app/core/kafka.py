import asyncio

from aiokafka import AIOKafkaProducer

loop = asyncio.get_event_loop()
# TODO: Use it the KAFKA env variables from config file
kafka_producer = AIOKafkaProducer(
    loop=loop, bootstrap_servers='localhost:9092'
)
