import redis
from facePhoto.settings import redis_pool


def get_redis_con():
    return redis.Redis(connection_pool=redis_pool)


