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
import redis
import collections
import numpy as np

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

conn = redis.Redis()

def buildHistogram():
    keys = conn.keys()
    values = conn.mget(keys)
    c = collections.Counter(values)
    z = sum(float(v) for v in values)
    print z
    print keys
    print values
    return {k : float(v)/float(z) for k,v in zip(keys, values)}

def entropy():
    keys = conn.keys()
    values = conn.mget(keys)
    c = collections.Counter(values)
    z = sum(float(v) for v in values)
    
    total = 0
    for k,v in zip(keys, values):
      val = float(v)/float(z)
      x = np.log(abs(val))
      y = x * val
      total -= y
    return json.dumps(total)

def probability(lang):
    h = buildHistogram()
    prob = h[lang]
    if prob > 0:
      print "Day: " + str(prob)
      return json.dumps({"day":prob})
    else:
      print "Night: " + str(prob)
      return json.dumps({"night":abs(prob)})

lang = sys.argv[1]

# Continue forever
while 1:

	entr = entropy()
	print entr
	if float(entr) >= .8:
		print "Posted a tweet"
		api.update_status("Entropy is very high!")
	
	prob = probability(lang)
	d = json.loads(prob)
	if 'day' in d:
		p = d['day']
		if float(p) >= .8:
			print "Posted a tweet"
			api.update_status("Probability is very high for day with language: " + lang)
	elif 'night' in d:
		p = d['night']
		if float(p) >= .8:
			print "Posted a tweet"
			api.update_status("Probability is very high for night with language: " + lang)

	# Sleep for 30 seconds - don't want to get rate limited by Twitter
	time.sleep(30)
