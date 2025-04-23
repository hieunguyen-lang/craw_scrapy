import redis

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def add_to_set(self, set_name, value):
        try:
            self.redis_client.sadd(set_name, value)
            print(f"✅ Added {value} to Redis set '{set_name}'")
        except Exception as e:
            print(f"❌ Error adding to Redis set: {e}")

    def is_member(self, set_name, value):
        try:
            return self.redis_client.sismember(set_name, value)
        except Exception as e:
            print(f"❌ Error checking membership in Redis set: {e}")
            return False

    def close(self):
        self.redis_client.close()