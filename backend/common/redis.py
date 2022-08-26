from datetime import timedelta
import redis

# We're using Redis as a way to store codes with expiry dates - it might a bit
# overkill, but it works

MINUTES_IN_DAY = 1440

cache = redis.Redis(host="redis", port=6379, db=0)

## EMAIL VERIFICATION

def add_verification(data, code):
    # We use a pipeline here to ensure these instructions are atomic
    pipeline = cache.pipeline()

    pipeline.hset(f"register:{code}", mapping=data)
    pipeline.expire(f"register:{code}", timedelta(hours=1))

    pipeline.execute()

def get_verification(code):
    key = f"register:{code}"

    if not cache.exists(key):
        return None

    result = {}

    for key, value in cache.hgetall(key).items():
        result[key.decode()] = value.decode()

    return result

## LOCKOUT

def register_incorrect(id):
    times = cache.get(f"attempts_{id}")

    if times is None:
        times = 0

    cache.set(f"attempts_{id}", int(times) + 1)

def incorrect_attempts(id):
    attempts = cache.get(f"attempts_{id}")

    if attempts is None:
        return 0
    else:
        return int(attempts)

def calculate_time(attempts):
    if attempts < 3:
        return 0
    
    minutes = 2 ** (attempts - 3)

    if minutes > MINUTES_IN_DAY:
        return MINUTES_IN_DAY
    else:
        return minutes

def block(id, time):
    cache.set(f"block_{id}", "", ex=timedelta(minutes=time))

def is_blocked(id):
    token = cache.get(f"block_{id}")
    return token is not None

## GENERAL FUNCTIONS

def clear_redis():
    cache.flushdb()