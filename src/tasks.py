"""Background tasks for the application."""
import base64
import json
from functools import wraps
import redis as red
from celery import Celery

worker = Celery(__name__, broker="amqp://guest:guest@localhost:5672//")

redis = red.Redis(host="cache", port=6379, db=0, decode_responses=True,encoding_errors="ignore")

def cache(ttl:int=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = base64.b64encode(f"{func.__name__}{args}{kwargs}".encode("utf-8")).decode("utf-8")
            if redis.exists(key):
                return json.loads(redis.get(key) or "")
            result = func(*args, **kwargs)
            redis.set(key, json.dumps(result), ex=ttl)
            return result
        return wrapper
    return decorator

def task(func):
    """Decorator for registering a function as a task."""
    worker.task(func)
    return func