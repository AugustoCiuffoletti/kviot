from flask import Flask, request, abort
from redis.client import Redis
import uuid
import json

conf = {}
app = Flask(__name__)
r = Redis()

with open('/etc/kviot.json', 'r') as fh: 
    conf=json.load(fh)

print(conf);
 
@app.route('/<key>',methods = ['GET','POST','PUT'])
def KVsvc(key):
##########
# GET
##########
	if request.method == 'GET':
# get value as a JSON string
		value = r.get(key)
		if ( value != None ):
# decode JSON value
			try:
				data = json.loads(value)
			except Exception as e:
				print(e)
				abort(500, "GET: Data error")
# find new key
			newKey = uuid.uuid4().hex[0:8]
			while ( r.exists(newKey) ):
				newKey = uuid.uuid4().hex[0:8]
# store value in new key
			r.set(newKey,value)
# delete old key
			if ( key != conf["masterKey"] ):
				r.delete(key)
# return value and the new key
			print(value)
			data[2]=newKey
			print(data)
			return json.dumps(data)
		else:
			abort(404, "GET: The key does not exists in the database")
##########
# POST
##########
	elif request.method == 'POST':
		data=request.get_data()
		print(data)
		print(key)
		if ( r.set(key,data,xx=True) is None ):
			abort(409, "PUT: The key does not exists in the database")
		return data
##########
# PUT
##########	
	elif request.method == 'PUT':
		data=request.get_data()
		if ( r.set(key,data,nx=True) is None ):
			abort(409, "PUT: The key already exists in the database")
		return data
	else:		
		return abort(405,"Only GET and POST methods are accepted on this route")

if __name__ == '__main__':
   app.run()
