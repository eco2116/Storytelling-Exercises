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