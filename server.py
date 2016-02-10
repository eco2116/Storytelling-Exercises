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
it = stream.statuses.filter(track='water')

for t in it:
	print json.dumps(t)
	sleep(5)

# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# stream = Stream(auth, l)
# stream_SFO = stream.filter(locations=[-122.75,36.8,-121.75,37.8], track=['python'],
# 	language="en")

# class StdOutListener(StreamListener):

# 	def __init__(self, api=None):
# 	    super(StdOutListener, self).__init__()
# 	    self.tweet_array = []
# 	    self.tweet_count = 0

# 	def on_status(self, status):
# 		record = {'Tweet text': status.text, 'Tweet time': status.created_at}
#         	print record
#         	sleep(8)

# PORT_NUMBER = 8111

# #This class will handles any incoming request from
# #the browser 
# class myHandler(BaseHTTPRequestHandler):
	
# 	#Handler for the GET requests
# 	def do_GET(self):
# 		self.send_response(200)
# 		self.send_header('Content-type','text/html')
# 		self.end_headers()

# 		#This handles Twitter authetification and the connection to Twitter Streaming API
# 		l = StdOutListener()
		
		
# 		#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
# 		return

# try:
# 	#Create a web server and define the handler to manage the
# 	#incoming request
# 	server = HTTPServer(('', PORT_NUMBER), myHandler)
# 	print 'Started httpserver on port ' , PORT_NUMBER
	
# 	#Wait forever for incoming htto requests
# 	server.serve_forever()

# except KeyboardInterrupt:
# 	print '^C received, shutting down the web server'
# 	server.socket.close()
	
