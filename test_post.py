#!/usr/bin/python
import json
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

if ( len(args) < 2  ):
	print("Servono la chiave ed il valore del campo 'id' come parametri")
	exit(1)

key =  args[0]
name = args[1]

payload = {
	"id": name,
	"tref": 18,
	"age": 0
}

value = [
		False,
		json.dumps(payload),
		""
		]

headers = {
	"ContentType": "application/json"
}

r = requests.post('http://' + url + '/' + key, json.dumps(value), headers = headers)

print(r.text)[:200]
