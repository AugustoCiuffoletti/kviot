#!/usr/bin/python
import json
import sys, getopt
from redis.client import Redis

masterkey = "12345678"

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

r = Redis(host=url)

payload = {
	"id": "Posto 7",
	"tref": 18,
	"age": 0
}

json_value = [
		False,
		json.dumps(payload),
		""
		]

if ( r.set(masterkey,json.dumps(json_value),nx=True) is None):
	print("Non eseguito, la chiave e' gia' presente")
else:
	print("Master key impostata!");
	print(r.get(masterkey))
