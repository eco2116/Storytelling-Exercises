
# Streaming JSON
# http://docs.python-requests.org/en/latest/user/advanced/#streaming-requests
# cite mike dewar github

import json
import requests
import redis
import time

r = requests.get('http://developer.usa.gov/1usagov', stream=True)

conn = redis.Redis()

last = 0
for line in r.iter_lines():

    # filter out keep-alive new lines
    if line:
		data = json.loads(line)

		try:
			timezone = data['tz']
		except KeyError:
			continue

		if data['tz'].startswith('America'):
			now = time.time()

			if last == 0:
				last = now
				continue

			delta = now - last
			conn.setex(now, delta, 120)
			print json.dumps({"time":now, "delta":delta, "timezone":data['tz']})
			last = now
