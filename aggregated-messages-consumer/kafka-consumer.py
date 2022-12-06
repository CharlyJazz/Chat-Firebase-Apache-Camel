from kafka import KafkaConsumer
import json

TOPIC_NAME = 'chat_messages_grouped'

consumer = KafkaConsumer(
  TOPIC_NAME,
  auto_offset_reset='latest'
  # value_deserializer=forgiving_json_deserializer
)

for msg in consumer:
  value = msg.value
  print('PRINT IN LOOP {}'.format(value))