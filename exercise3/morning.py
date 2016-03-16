#########################################
# Evan O'Connor	
# eco2116
# Storytelling and Streaming Data  
# exercise 3
# morning.py 
#########################################

# This script tracks tweets that either mention good morning or good
# morning. It prints a JSON dump of the tweet, the language of the tweet,
# and a "time", which is either night or morning, in this case morning.
# count.py will read in from this JSON dump, notice that morning was chosen,
# and update the redis DB accordingly. Capturing a data point from this
# stream could possibly indicate to us that people are going to bed
# in the given location. While the language does not explicitly imply
# the geographic location of users, it is our best indicator, as all
# other twitter geolocators are rarely included in Twitter's response.
# While the distribution of morning/night may be difficult to understand
# in a geographic sense by using something such as lanugage, it provides
# us with a general approach to the problem, and in the future, if Tweets
# start containing more geographic details, we could implement it as such.

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

it = stream.statuses.filter(track='good morning')

for t in it:
	try:
		msg = t["text"]
		lang = t["lang"]
	except KeyError:
			continue
	print json.dumps({"msg" : msg, "lang" : lang, "time" : "morning"})
	sys.stdout.flush()
	sleep(.5)