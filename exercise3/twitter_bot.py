#########################################
# Evan O'Connor	
# eco2116
# Storytelling and Streaming Data  
# exercise 3
# twitter_bot.py 
#########################################

# This script takes in a language as a command line argument. It then
# connects to redis, assuming that the morning/night scripts and the
# count scripts have been run (see README for use). It then tracks
# the entropy of the system and the probability of receiving a good morning
# or goodnight tweet for the specified language. It will send a tweet
# to my account of any of these values are unusually high.

# Source used for Twitter bot:
# http://www.dototot.com/how-to-write-a-twitter-bot-with-python-and-tweepy/

import tweepy # Used to post to twitter
import sys # Used to read in from stdin (specifically, alerted averages from alert_system.py)
import time # Used to sleep for 30 seconds between postings - Don't want to get rate limited by Twitter
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

# Create histogram according to Mike Dewar's process
def buildHistogram():
    keys = conn.keys()
    values = conn.mget(keys)
    c = collections.Counter(values)
    z = sum(float(v) for v in values)
    print z
    print keys
    print values
    return {k : float(v)/float(z) for k,v in zip(keys, values)}

# Entropy calculation following Mike Dewar's description. A high entropy
# value would indicate to us that rapid change is occuring in our
# rate tracking for this stream.
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

# Returns the probability that a given good morning or good night tweet
# will appear given the current distribution. The probability function
# must take in a language for which it will perform the probability calculation on.
def probability(lang):
    h = buildHistogram()
    prob = h[lang]
    if prob > 0:
      print "Day: " + str(prob)
      return json.dumps({"day":prob})
    else:
      print "Night: " + str(prob)
      return json.dumps({"night":abs(prob)})

# First argument (required) to this function is the language to get the probability
# of receiving a good morning/night tweet at that moment for.
lang = sys.argv[1]

# Continue forever
while 1:

  # Alert user if entropy is unusually high
	entr = entropy()
	print entr
	if float(entr) >= .8:
		print "Posted a tweet"
		api.update_status("Entropy is very high!")
	
  # Alert user if the probability is high either for a good morning or a 
  # good night tweet for the language provided
	prob = probability(lang)
	d = json.loads(prob)
	if 'day' in d:
		p = d['day']
		if float(p) >= .8:
			print "Posted a tweet"
			api.update_status("Probability is very high for day with language: " + lang + ": " + str(p))
	elif 'night' in d:
		p = d['night']
		if float(p) >= .8:
			print "Posted a tweet"
			api.update_status("Probability is very high for night with language: " + lang + ": " + str(p))

	# Sleep for 30 seconds - don't want to get rate limited by Twitter
	time.sleep(30)
