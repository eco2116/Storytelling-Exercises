import sys
from SimpleHTTPServer import SimpleHTTPRequestHandler as HandlerClass
from tweepy.streaming import StreamListener
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
from time import sleep
from twitter import OAuth, Twitter, TwitterStream

from tweepy import OAuthHandler
from tweepy import Stream

access_token = "4889482000-F8lBrL3pTHafiQO80UYXaAOnQrwT4xIy3mfjtrk"
access_token_secret = "VumeBLAn81CjYnix7FgLL3aLb6B4Urfe7WcprTRfk796z"
consumer_key = "kMKv0tJLjW7HZs0CiWaYFdq01"
consumer_secret = "yUxhzsWXn1TSCzkIEeUIHQKCZyI7PabLaNeFSDLwC2voGg9irV"

auth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
stream = TwitterStream(auth=auth)
it = stream.statuses.filter(track='safe water', locations='43,-84,44,-83')

for t in it:
	print json.dumps(t)
	sleep(5)

