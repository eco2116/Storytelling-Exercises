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

## Continue reading forever
while 1:

	# Read a line from std in and decode it into JSON format using python's JSON library
	line = sys.stdin.readline()
	d = json.loads(line)

	# Pull the avg rate from the JSON read in
	rate = d['rate']

	# Alert the user if the rate is negative - this doesn't make sense. Something is fishy.
	if rate < 0:
		print "Alert! Negative rate: " + str(rate)

	# Alert the user if the rate is unusually high - above 3 is a good gauge for this as it is relatively
	# unusual, but not impossible. The user may want to be notified of such a high rate.
	else if rate > 3:
		print "Alert! Rate is very high: " + str(rate)

	# Now, we are going to see if the rate is making sudden jumps between successive measurements
	# First we check to see if we are examining the first record, in which case we need to skip to find
	# another record to examine to find the change in rate.
	last = 0
	if last == 0:
		last = rate
		continue

	# This is not the first rate measurement, so we can calculate a difference and alert the user
	# if the rate has made an unusually large jump either upwards or downwards.
	diff = last - rate
	if diff > .3 || diff < -.3:
		print "Alert! Very large rate change: " + str(rate)

