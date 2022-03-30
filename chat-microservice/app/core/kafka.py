import asyncio

from aiokafka import AIOKafkaProducer
from app.core.config import settings

loop = asyncio.get_event_loop()

kafka_producer = AIOKafkaProducer(
    loop=loop, 
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER
)
