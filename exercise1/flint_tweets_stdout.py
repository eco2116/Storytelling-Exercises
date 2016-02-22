####################################################
# Evan O'Connor
# eco2116
# Storytelling & Streaming Data
# Homework 1
# flint_tweets_stdout.py
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

# Iterate through tweets filtering out and pritty printing relevant data
count = 1
for t in it:
	tweet = json.dumps(t)
	data = json.loads(tweet)
	print "Tweet number in stream: " + str(count)
	print "Tweet message: " + data['text']
	print "Tweet time: " + data['created_at'] + "\n"
	count += 1
	sleep(2)