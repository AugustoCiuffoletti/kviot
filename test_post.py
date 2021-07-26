#!/usr/bin/python

import json
import sys
import requests

if ( len(sys.argv) <= 2  ):
	print("Servono la chiave ed il valore del campo 'id' come parametri")
	exit(1)

url = "127.0.0.1"
key =  sys.argv[1]
name = sys.argv[2]

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

r = requests.post('http://' + url + '/' + key, headers = headers, data=json.dumps(value))

print(r.text)[:200]
