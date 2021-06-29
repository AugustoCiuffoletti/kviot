from flask import Flask, request, abort
from redis.client import Redis
import uuid
import json
 
app = Flask(__name__)
r = Redis()
 
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
		if ( r.exists(key) ):
			r.set(key,data)
			return data
		else:
			abort(404, "POST: The key does not exists in the database")
##########
# PUT
##########	
	elif request.method == 'PUT':
		data=request.get_data()
		if ( r.exists(key) ):
			abort(409, "PUT: The key already exists in the database")
		else:
			r.set(key,data)
			return data
	else:		
		return abort(405,"Only GET and POST methods are accepted on this route")
			
@app.route('/new/<key>')
def NewKey(key):
	# Qui dovrei mettere una transazione atomica tra exists e set
	if ( r.exists(key) == 0 ):
		r.set(key,"NULL")
		return key
	else:
		print("Occupata")
		abort(409,"The key already exists in the database")

if __name__ == '__main__':
   app.run()
