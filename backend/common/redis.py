import redis

# We're using Redis as a way to store codes with expiry dates - it might a bit
# overkill, but it works

cache = redis.Redis(host="redis", port=6379, db=0)
