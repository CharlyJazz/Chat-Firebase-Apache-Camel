from kafka import KafkaConsumer

TOPIC_NAME = 'chat_messages'
consumer = KafkaConsumer(TOPIC_NAME)

for msg in consumer:
  print(msg)
