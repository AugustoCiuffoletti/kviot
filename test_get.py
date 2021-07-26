#!/usr/bin/python
import sys
import requests

if ( len(sys.argv) <= 1  ):
	print("Serve la chiave come parametro")
	exit(1)

url = "127.0.0.1"
key =  sys.argv[1]

headers = {
	"ContentType": "application/json"
}

r = requests.get('http://' + url + '/' + key, headers = headers)

print(r.text)[:200]
