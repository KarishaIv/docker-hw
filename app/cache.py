import redis

r = redis.Redis(host="redis", port=6379, db=0)

def get_from_cache(code):
    result = r.get(code)
    return result.decode() if result else None

def set_to_cache(code, url):
    r.setex(code, 3600, url)
