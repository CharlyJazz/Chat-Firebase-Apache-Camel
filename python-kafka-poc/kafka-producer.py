from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092']
  )

# Asynchronous by default
producer.send('chat', b'raw_bytes')
# Leer esta verga
# https://stackoverflow.com/questions/45092857/kafka-produce-send-never-sends-the-message?rq=1
producer.flush()
