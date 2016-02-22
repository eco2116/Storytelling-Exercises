
# cite http://www.dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/

import tweepy
import sys
import time
import json

#Twitter provided keys and secrets
access_token = "4889482000-F8lBrL3pTHafiQO80UYXaAOnQrwT4xIy3mfjtrk"
access_token_secret = "VumeBLAn81CjYnix7FgLL3aLb6B4Urfe7WcprTRfk796z"
consumer_key = "kMKv0tJLjW7HZs0CiWaYFdq01"
consumer_secret = "yUxhzsWXn1TSCzkIEeUIHQKCZyI7PabLaNeFSDLwC2voGg9irV"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

while 1:
	line = sys.stdin.readline()
	d = json.loads(line)
	rate = d['rate']
	print rate
	if rate > 1:
		print "posted a tweet!"
		api.update_status("Alert: rate is " + str(rate))
		time.sleep(900)