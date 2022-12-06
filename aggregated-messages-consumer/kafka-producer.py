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
    "from_user": "charlyjazz",
    "to_user": "other_user",
    "body": "Hello other user",
    "chat_id": 2
  },
  {
    "from_user": "charlyjazz",
    "to_user": "evil",
    "body": "Hello bro",
    "chat_id": 1
  },
  {
    "from_user": "evil",
    "to_user": "charlyjazz",
    "body": "What?",
    "chat_id": 1
  },
  {
    "from_user": "charlyjazz",
    "to_user": "evil",
    "body": "Pepe le pu",
    "chat_id": 1
  },
  {
    "from_user": "evil",
    "to_user": "charlyjazz",
    "body": "Ohh I see",
    "chat_id": 1
  },
  {
    "from_user": "charlyjazz",
    "to_user": "evil",
    "body": "Bye bro",
    "chat_id": 1
  }
]

for i in MESSAGES:
    producer.send('chat_messages', json.dumps(i).encode('utf-8'))
    producer.flush()
