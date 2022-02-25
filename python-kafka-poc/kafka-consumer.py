from kafka import KafkaConsumer

consumer = KafkaConsumer('chat')
for msg in consumer:
  print(msg)
