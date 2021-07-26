#!/usr/bin/python
import json
from redis.client import Redis

masterkey = "34567890"

r = Redis()

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
