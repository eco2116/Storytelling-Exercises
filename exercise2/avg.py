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

	# Get keys from redis, the exact time data was received
	keys = conn.keys()

	# Get the values from redis corresponding to these keys
	# (time differences between the key time and the last time data was received)
	values = conn.mget(keys)

	# Attempt to read in float values (moving averages)
	try:
		deltas = [float(v) for v in values]
	# If the values are not floats, skip and try again. This shouldn't happen
	# if the proper scripts / pipeline is used.
	except TypeError:
		continue

	# If data is found, calculate the average rate from all time differences read in
	# by dividing sum of time differences by number of time differences. This is
	# the moving average
	if len(deltas):
		rate = sum(deltas)/float(len(deltas))

	# Rate is 0 if no data read in
	else:
		rate = 0

	# Print out the rate as JSON to stdout to be read in by alert_system.py
	print json.dumps({"rate":rate})

	# Flush the output
	sys.stdout.flush()

	# Sleep for 2 seconds - only calculate moving average every two seconds.
	time.sleep(2)
