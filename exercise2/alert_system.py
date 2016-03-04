#########################################
# Evan O'Connor							#
# eco2116							    #
# Storytelling and Streaming Data       #
# exercise 2						    #
# alert_system.py                       #
#########################################

# This script reads in the average rate that Government URLS are shortened using Bitly
# which is piped from avg.py. It checks for unusually low or unusually high rates and
# alerts the user by writing to stdout. It also checks for unusually large jumps
# between two consecutive rate measurements.

import sys # Used for reading in from stdin
import json # Used for decoding JSON data
from time import sleep

last = 0 # Used for checking if we only have one piece of data and cannot calculate a difference

# Continue reading forever
while 1:
	sleep(1)
	# Read a line from std in and decode it into JSON format using python's JSON library
	line = sys.stdin.readline()
	d = json.loads(line)

	# Pull the avg rate from the JSON read in
	rate = d['rate']

	# Alert the user if the rate is negative - this doesn't make sense. Something is fishy.
	if rate < 0:
		print json.dumps({"status": "Alert! Negative rate: " + str(rate)})
		sys.stdout.flush() # flush status to stdout to be read by twitter_bot.py

	# Alert the user if the rate is unusually high - above 1 is a good gauge for this as it is relatively
	# unusual, but not impossible. The user may want to be notified of such a high rate.
	if rate > 1:
		print json.dumps({"status": "Alert! Rate is very high: " + str(rate)})
		sys.stdout.flush() # flush status to stdout to be read by twitter_bot.py

	# Now, we are going to see if the rate is making sudden jumps between successive measurements
	# First we check to see if we are examining the first record, in which case we need to skip to find
	# another record to examine to find the change in rate.
	if last == 0:
		last = rate
		continue

	# This is not the first rate measurement, so we can calculate a difference and alert the user
	# if the rate has made an unusually large jump either upwards or downwards.
	diff = last - rate
	
	# If moving average grows or drops by more than .01, this is unusual. Alert the user.
	if diff > .01 or diff < -.01:
		print json.dumps({"status": "Alert! Very large rate change: " + str(rate)})
		sys.stdout.flush() # flush status to stdout to be read by twitter_bot.py

	last = rate
