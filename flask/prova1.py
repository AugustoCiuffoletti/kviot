from redis.client import Redis
r = Redis()
print(r.get("Bahamas"))
