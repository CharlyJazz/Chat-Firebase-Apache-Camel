from app.core.kafka import kafka_producer
from app.models.chat_messages import ChatMessages

"""
Kafka Producer instance as dependency in order to easy mock it
"""
def get_kafka_producer():
    return kafka_producer

"""
Model as dependency in order to easy mock it
"""
def get_chat_message_model():
    return ChatMessages
