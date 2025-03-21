import redis
from app.config import REDIS_URL

# 创建Redis客户端
redis_client = redis.from_url(REDIS_URL)

def get_redis():
    """获取Redis客户端"""
    return redis_client 