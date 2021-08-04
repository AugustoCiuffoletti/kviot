#!/usr/bin/python
import sys, getopt
import requests

#default
url = "127.0.0.1"

opts, args = getopt.getopt(sys.argv[1:], "r")

for opt, arg in opts:
	if opt == '-r':
         url = "192.168.113.181"
         print("Querying the Raspberry")
	else:
		print "Not a legal option"
		exit(1)

if ( len(args) < 1  ):
	print("Serve la chiave come parametro")
	exit(1)

key =  args[0]

headers = {
	"ContentType": "application/json"
}

r = requests.get('http://' + url + '/' + key, headers = headers)

print(r.text)[:200]
