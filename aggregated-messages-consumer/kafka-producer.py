from kafka import KafkaProducer
from datetime import datetime
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092']
)

# https://stackoverflow.com/questions/45092857/kafka-produce-send-never-sends-the-message?rq=1

MESSAGES = [
  {
    "from_user": "charlyjazz",
    "to_user": "other_user",
    "body": "Hello other user",
    "chat_id": 2,
    "message_id": 1,
    "time": str(datetime.today())
  },
  {
    "from_user": "charlyjazz",
    "to_user": "evil",
    "body": "Hello bro",
    "chat_id": 1,
    "message_id": 2,
    "time": str(datetime.today())
  },
  {
    "from_user": "evil",
    "to_user": "charlyjazz",
    "body": "What?",
    "chat_id": 1,
    "message_id": 3,
    "time": str(datetime.today())
  },
  {
    "from_user": "charlyjazz",
    "to_user": "evil",
    "body": "Pepe le pu",
    "chat_id": 1,
    "message_id": 4,
    "time": str(datetime.today())
  },
  {
    "from_user": "evil",
    "to_user": "charlyjazz",
    "body": "Ohh I see",
    "chat_id": 1,
    "message_id": 5,
    "time": str(datetime.today())
  },
  {
    "from_user": "charlyjazz",
    "to_user": "evil",
    "body": "Bye bro",
    "chat_id": 1,
    "message_id": 6,
    "time": str(datetime.today())
  }
]

for i in MESSAGES:
    producer.send('chat_messages', json.dumps(i).encode('utf-8'))
    producer.flush()
