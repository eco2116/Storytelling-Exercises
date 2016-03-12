import redis
import time

conn = redis.Redis()

while True:

    langs = conn.keys()

    for lang in langs:

        d = conn.hgetall(lang)

        for t in d:
            if int(d[t]) > 1:
                count = int(d[t])
                count -= 1
                d[t] = str(count)

        conn.hmset(lang,d)

    time.sleep(2)


