from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092']
  )

# Asynchronous by default
# producer.send('chat', b'raw_bytes')
# Leer esta verga
# https://stackoverflow.com/questions/45092857/kafka-produce-send-never-sends-the-message?rq=1

MESSAGES = [
  {
    "user_id": "charlyjazz",
    "message": "Hello bro"
  },
  {
    "user_id": "evil",
    "message": "What?"
  },
    {
    "user_id": "charlyjazz",
    "message": "Pepe le pu"
  },
  {
    "user_id": "evil",
    "message": "Ohh I see"
  },
  {
    "user_id": "charlyjazz",
    "message": "Bye bro"
  }
]

for i in MESSAGES:
    producer.send('chat', json.dumps(i).encode('utf-8'))
    producer.flush()
