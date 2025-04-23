import pika
import json

credentials = pika.PlainCredentials('admin', 'admin')
params = pika.ConnectionParameters(
    host='mysql',
    port=5672,
    virtual_host='/',
    credentials=credentials
)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='data_crawled', durable=True)

message = {"title": "Hello", "description": "Test"}
channel.basic_publish(
    exchange='',
    routing_key='data_crawled',
    body=json.dumps(message),
    properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
)

print("Sent!")
connection.close()
