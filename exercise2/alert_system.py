import sys
import json

while 1:
	line = sys.stdin.readline()
	d = json.loads(line)
	rate = d['rate']
	if rate > 2:
		print "Alert! Rate is: " + str(rate)
