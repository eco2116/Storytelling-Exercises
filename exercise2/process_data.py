#########################################
# Evan O'Connor
# eco2116
# Storytelling and Streaming Data
# exercise 2
# process_data.py
#########################################

# This script requests the data feed from usa.gov which sends data representing instances when
# "USA.gov URLs are created whenever anyone shortens a .gov or .mil URL using bitly.com"
# (source: https://www.usa.gov/developer). The data stream is located at the URL
# http://developer.usa.gov/1usagov. This script prints to stdout the time that the data was
# received, the elapsed time since the last data was received, and the timezone from which
# the data came from. I chose to filter to only capture data coming from American timezones.
# The script also stores this information in redis to be used by avg.py.

# Source used for streaming JSON:
# http://docs.python-requests.org/en/latest/user/advanced/#streaming-requests
#
# Source used for redis / rate calculation example:
# https://github.com/mikedewar/RealTimeStorytelling

import json # Used for decoding JSON data
import requests # Used to request data stream from USA.gov
import redis # Used to store delta values, used later to calculate average rate
import time # Used to calculate time data is received

# Make a streaming connection to desired USA.gov data stream
r = requests.get('http://developer.usa.gov/1usagov', stream=True)

conn = redis.Redis() # Set up redis connection

last = 0 # Last is used to ensure we have to consecutive data points to caluclate a time difference

# Will continue as long as the stream provides data (ideally forever)
for line in r.iter_lines():

    # Filter out keep-alive new lines
    if line:

    	# Decode JSON data sent from USA.gov using python's JSON library
		data = json.loads(line)

		# Pull out the timezone of the data
		try:
			timezone = data['tz']
		# Some data does not have a timezone. That is okay, just skip over that point.
		except KeyError:
			continue

		# Only use data if the timezone begins with America, ie: America/New_York. American timezones
		# will always start with the country code (America) followed by a city code (New_York).
		if data['tz'].startswith('America'):

			# Capture the current time the data is processed
			now = time.time()

			# If this is the first piece of data we have received, continue on to find another piece.
			# We cannot calculate a time difference with only one piece of data, so continue on without
			# calculating the difference.
			if last == 0:
				last = now
				continue

			# Calculate the difference, knowing we have 2 data points to compare.
			delta = now - last

			# Store in redis the current time and the time difference since the last piece of data 
			# was received
			conn.setex(now, delta, 120)

			# Print to stdout the time data was received, the time difference since the last piece
			# of data was received, and the timezone
			print json.dumps({"time":now, "delta":delta, "timezone":data['tz']})

			# The current piece of data is set as the last piece of data, to be used in the
			# next difference calculation.
			last = now
