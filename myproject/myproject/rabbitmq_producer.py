import pika
import json
import redis
from myproject.redis_client import RedisClient
class RabbitMQClient:
    def __init__(self, host='localhost', port=5672, username='admin', password='admin'):
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host='/',
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        # self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
        self.redis_client = RedisClient()
    def send_to_rabbitmq(self, queue_name, message):
        #print("📤 Đang gửi tới RabbitMQ:", message)
        # Đảm bảo queue tồn tại và bền vững
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
            # Kiểm tra trùng lặp trong Redis
            message_id = message.get("url")  # Giả sử message có trường "message_id"
            
            if self.redis_client.is_member("message_ids_set", message_id):
                print(f"⚠️ Message with ID {message_id} already exists in Redis. Skipping sending to queue.")
                return  # Nếu thông điệp đã tồn tại, bỏ qua
            # Gửi thông điệp với delivery_mode=2 (persistent)
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2  # Persistent message
                )
            )
             # Lưu trữ message_id vào Redis để kiểm tra trùng lặp lần sau
            self.redis_client.add_to_set("message_ids_set", message_id)
            print(f"✅ Sent message to queue '{queue_name}': {message.get('url')}")
        except Exception as e:
            print(f"❌ Lỗi khi gửi message: {e}")
            

    def close(self):
        self.connection.close()