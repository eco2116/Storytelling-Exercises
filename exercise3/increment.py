import json
import sys
import redis
import time
import urlparse

conn = redis.Redis()

while 1:
    line = sys.stdin.readline()
    try:
        d = json.loads(line)
    except ValueError:
        # sometimes we get an empty line, so just skip it
        continue

    try:
        time = d["time"]
    except KeyError:
        # if there is no city present in the message
        # then let's just ditch it
        continue

    try:
        lang = d["lang"]
    except KeyError:
        # if there is no referrer present in the message
        # then let's just ditch it
        continue

    if time == "morning":
        conn.incr(lang, 1)
    elif time == "night":
        conn.decr(lang, 1)
    #conn.hincrby(lang, time, 1)

    print json.dumps({"lang": lang, "time": time})
    sys.stdout.flush()
