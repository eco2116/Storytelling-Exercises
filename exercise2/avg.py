#########################################
# Evan O'Connor							#
# eco2116							    #
# Storytelling and Streaming Data       #
# exercise 2						    #
# avg.py                      	        #
#########################################

# This script connects to redis and reads in the total number of time difference
# measurements performed by process_data.py. It uses this to create a running
# average of the time difference between collected datapoints, or a moving average.
# It prints this moving average to stdout, so that the alert system can read in
# the data and determine when to alert the user via its own stdout.

# Source used for understanding redis pipelining:
# http://redis.io/topics/pipelining
#
# Source used for redis / rate calculation example:
# https://github.com/mikedewar/RealTimeStorytelling

import redis # Used for reading in time differences to calculate moving average
import json # Used for decoding JSON
import sys # Used for flushing data to stdout
import time # Used for sleeping, so rate is calculate at chosen intervals

# Create a connection to redis
conn = redis.Redis()

# Continue forever
while 1:

	# Create redis pipeline so we can send multiple commands to server 
	# without waiting for response and read them in at once
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
