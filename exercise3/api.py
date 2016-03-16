#########################################
# Evan O'Connor 
# eco2116
# Storytelling and Streaming Data  
# exercise 3
# api.py 
#########################################

# This implementation is helpful, because we can call it from outside 
# sources (even the browser in this example because we enabled
# cross domain requests) at different times. Therefore, we can track point-to-point
# changes in each of the tracking metrics. The distribution uses a histogram-style
# technique to show us real-time counts of morning/night tweet distributions in real
# time based on the languages of the tweets. A geographic locaiton would be more
# interesting to track, but most Tweets do not contain one, while the majority at least
# have a language. Also, of course, we are tracking an english phrase, so the majority
# of the responses will be for 'en' language. This is expected. No matter, it is still
# an interesting application and quite a few other-language tweets are still being 
# tracked. The entropy calculation, based on Mike Dewar's implementation in class,
# which uses the idea that the differential entropy can be approximated by producing
# a histogram of observations and finding the discrete entropy of that histogram. In
# this case, the discrete observations are good morning or good night tweets.
# The probability endpoint takes in a given language and produces the probability
# given the current distribution of receiving a good morning or good night tweet.
# Essentially, if we get back a negative number internally, we understand that this
# just means the equivalent positive probability that a night tweet (decrementing)
# will be returned. So, we just return the absolute value because probabilities must
# be positive. 

import flask
from flask import request
import redis
import collections
import json
import numpy as np
from flask.ext.cors import CORS, cross_origin

# To install CORS dependency run: pip install -U flask-cors
app = flask.Flask(__name__)
conn = redis.Redis()
CORS(app)

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

# Distribution just returns a histogram. We need cross origin domain support
# to display the distribution in the browser.
@app.route("/distribution")
@cross_origin()
def histogram():
    h = buildHistogram()
    return json.dumps(h)

# The rate is a sum of all of the values in the distribution weighted evenly.
# This value describes the general, overall, worlwide count of people tweeting
# good morning vs. good night
@app.route("/rate")
def rate():
    keys = conn.keys()
    values = conn.mget(keys)
    c = collections.Counter(values)
    z = sum(float(v) for v in values)
    return json.dumps(z)

# Entropy calculation following Mike Dewar's description. A high entropy
# value would indicate to us that rapid change is occuring in our
# rate tracking for this stream.
@app.route("/entropy")
def entropy():
    keys = conn.keys()
    values = conn.mget(keys)
    c = collections.Counter(values)
    z = sum(float(v) for v in values)
    
    # Perform mike dewar's calculation
    total = 0
    for k,v in zip(keys, values):
      val = float(v)/float(z)
      x = np.log(abs(val))
      y = x * val
      total -= y
    return json.dumps(total)

# Returns the probability that a given good morning or good night tweet
# will appear given the current distribution
@app.route("/probability")
def probability():
    lang = request.args.get('lang', '')
    h = buildHistogram()
    prob = h[lang]
    # We can't have a negative probability, so just display positive probabilities
    # as either probabilities leaning towards receiving day or night tweets.
    if prob > 0:
      print "Day: " + str(prob)
      return json.dumps({"day":prob})
    else:
      print "Night: " + str(prob)
      return json.dumps({"night":abs(prob)})

if __name__ == "__main__":
    app.debug = True
    app.run()
