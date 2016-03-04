#########################################
# Evan O'Connor	
# eco2116
# Storytelling and Streaming Data  
# exercise 2
# twitter_bot.py 
#########################################

# This script reads in JSON data outputted from alert_system.py, reading in
# various alert messages when rates exceed normal values or experience unusually
# large changes. The script then opens an OAuth connection and uses
# Python's tweepy library to post tweets to my test Twitter account with
# the alert status read in. The script sleeps 30 seconds after each tweet
# so as not to risk exceeding Twitter's rate limit.

# Source used for Twitter bot:
# http://www.dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/

import tweepy # Used to post to twitter
import sys # Used to read in from stdin (specifically, alerted averages from alert_system.py)
import time # Used to sleep for 900 seconds between postings - Don't want to get rate limited by Twitter
import json # Used to decode JSON data

# Twitter provided keys and secrets for my Twitter: @columbiaeco2116
access_token = "4889482000-F8lBrL3pTHafiQO80UYXaAOnQrwT4xIy3mfjtrk"
access_token_secret = "VumeBLAn81CjYnix7FgLL3aLb6B4Urfe7WcprTRfk796z"
consumer_key = "kMKv0tJLjW7HZs0CiWaYFdq01"
consumer_secret = "yUxhzsWXn1TSCzkIEeUIHQKCZyI7PabLaNeFSDLwC2voGg9irV"

# Set up OAuth Handler to be used to verify to Twitter that we are verified to send Tweets
# This is set up using the consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Set the access token on OAuth using the access token and access token secret
auth.set_access_token(access_token, access_token_secret)

# Create an API object using Python's Twitter helper library, tweepy
api = tweepy.API(auth)

# Continue forever
while 1:

	# Read in a line from stdin - reading rate alerts from alert_system.py
	line = sys.stdin.readline()

	# Decode JSON data from stdin
	d = json.loads(line)
	print d
	# Pull out the moving average, or "rate" from the alert system
	status = d['status']

	# Print to standart out that a Tweet was posted. Print the status.
	print "Posted a tweet!"
	print status

	# Post a tweet with the alert message send from avg.py
	api.update_status(status)

	# Sleep for 30 seconds - don't want to get rate limited by Twitter
	time.sleep(30)
