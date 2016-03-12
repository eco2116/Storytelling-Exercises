import flask
from flask import request
import redis
import collections
import json
import numpy as np

app = flask.Flask(__name__)
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
    #return {k:v/float(z) for k,v in c.items()}

@app.route("/distribution")
def histogram():
    h = buildHistogram()
    return json.dumps(h)

@app.route("/rate")
def rate():
    keys = conn.keys()
    values = conn.mget(keys)
    c = collections.Counter(values)
    z = sum(float(v) for v in values)
    return json.dumps(z)

@app.route("/entropy")
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

@app.route("/probability")
def probability():
    lang = request.args.get('lang', '')
    h = buildHistogram()
    prob = h[lang]
    if prob > 0:
      print "Day: " + str(prob)
      return json.dumps({"day":prob})
    else:
      print "Night: " + str(prob)
      return json.dumps({"night":abs(prob)})




if __name__ == "__main__":
    app.debug = True
    app.run()
