####################################################
# Evan O'Connor
# eco2116
# Storytelling & Streaming Data
# Homework 1
# flint_tweets_webpage.py
####################################################

import json
from time import sleep
from twitter import OAuth, Twitter, TwitterStream

#Twitter provided keys and secrets
access_token = "4889482000-F8lBrL3pTHafiQO80UYXaAOnQrwT4xIy3mfjtrk"
access_token_secret = "VumeBLAn81CjYnix7FgLL3aLb6B4Urfe7WcprTRfk796z"
consumer_key = "kMKv0tJLjW7HZs0CiWaYFdq01"
consumer_secret = "yUxhzsWXn1TSCzkIEeUIHQKCZyI7PabLaNeFSDLwC2voGg9irV"

# Set up authorization using Twitter-provided keys and secrets
auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)

# Begin a new Twitter stream using OAuth
stream = TwitterStream(auth=auth)

# Stream only tweets that contain the 'water' in the text, written near Flint Michigan
it = stream.statuses.filter(track='water', locations='43.0,-83.8,43.1,-83.7')

# Iterate through tweets passing raw JSON to be filtered by JS in the webpage
for t in it:
	print json.dumps(t)
	sleep(2)