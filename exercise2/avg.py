import redis
import json
import sys
import time

conn = redis.Redis()

while 1:

	pipe = conn.pipeline()
	keys = conn.keys()
	values = conn.mget(keys)

	try:
		deltas = [float(v) for v in values]
	except TypeError:
		continue

	if len(deltas):
		rate = sum(deltas)/float(len(deltas))
	else:
		rate = 0

	print json.dumps({"rate":rate})
	sys.stdout.flush()

	time.sleep(2)
