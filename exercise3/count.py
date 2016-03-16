#########################################
# Evan O'Connor 
# eco2116
# Storytelling and Streaming Data  
# exercise 3
# count.py 
#########################################

# This script reads in from either morning.py or night.py. It simply increments
# a count (if reading a good morning message) or decrements a count (if reading
# a goodnight message) based in redis for a given language. By default if no
# index for the given language exists, redis will initialize it properly (one
# decrement = -1 and one increment = +1). The implementation is based on Mike Dewar's
# example given in class.

import json
import sys
import redis
import time
import urlparse

# Connect to redis
conn = redis.Redis()

while 1:
    line = sys.stdin.readline()
    try:
        # Try to load a line of JSON - if it doesn't work, keep reading
        d = json.loads(line)
    except ValueError:
        continue

    try:
        # Try to get the time - skip if it doesn't exist and find next one
        time = d["time"]
    except KeyError:
        continue

    try:
        # Try to get the language - skip if it doesn't exist and find next one
        lang = d["lang"]
    except KeyError:
        continue

    # Morning vs. night count update
    if time == "morning":
        # Increment the count - we received a good morning tweet
        conn.incr(lang, 1)
    elif time == "night":
        # Decrement the count - we received a good night tweet
        conn.decr(lang, 1)

    # Print out JSON of the language and time of receiving the tweet
    print json.dumps({"lang": lang, "time": time})
    sys.stdout.flush()
