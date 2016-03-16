#########################################
# Evan O'Connor	
# eco2116
# Storytelling and Streaming Data  
# exercise 2
# night.py 
#########################################

# This script takes in a language as a command line argument. It then
# connects to redis, assuming that the morning/night scripts and the
# count scripts have been run (see README for use). It then tracks
# the entropy of the system and the probability of receiving a good morning
# or goodnight tweet for the specified language. It will send a tweet
# to my account of any of these values are unusually high.

import json
from time import sleep
from twitter import OAuth, Twitter, TwitterStream
import sys

#Twitter provided keys and secrets
access_token = "4889482000-F8lBrL3pTHafiQO80UYXaAOnQrwT4xIy3mfjtrk"
access_token_secret = "VumeBLAn81CjYnix7FgLL3aLb6B4Urfe7WcprTRfk796z"
consumer_key = "kMKv0tJLjW7HZs0CiWaYFdq01"
consumer_secret = "yUxhzsWXn1TSCzkIEeUIHQKCZyI7PabLaNeFSDLwC2voGg9irV"

# Set up authorization using Twitter-provided keys and secrets
auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)

# Begin a new Twitter stream using OAuth
stream = TwitterStream(auth=auth)

it = stream.statuses.filter(track='good night')

for t in it:
	try:
		msg = t["text"]
		lang = t["lang"]
	except KeyError:
			continue
	print json.dumps({"msg" : msg, "lang" : lang, "time" : "night"})
	sys.stdout.flush()
	sleep(.5)