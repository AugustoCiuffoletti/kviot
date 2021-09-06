from flask import Flask, request, abort
from redis.client import Redis
import uuid
import json
import logging
import time

conf = {}
loglevel=[logging.DEBUG,logging.INFO,logging.WARNING,logging.ERROR,logging.CRITICAL]
app = Flask(__name__)
r = Redis()

with open('/etc/kviot.json', 'r') as fh: 
    conf=json.load(fh)
    
logging.basicConfig(filename='/var/log/kviot.log', encoding='utf-8', level=loglevel[conf["loglevel"]])

print(conf);
logging.info("========== New Service Starting ===========")
@app.route('/<key>',methods = ['GET','POST','PUT','HEAD'])
def KVsvc(key):
##########
# GET
##########
	if request.method == 'GET':
		logging.info(str(time.time()) + ": " + "GET " + request.remote_addr + ' ' + key) #T0
# get value as a JSON string
		value = r.get(key)
		if ( value is not None ):
# decode JSON value
			try:
				data = json.loads(value)
				logging.info(str(time.time()) + ":  " + str(value, 'UTF-8')) #T1
			except Exception as e:
				logging.critical(str(time.time()) + ": Not a JSON string")
				abort(500, "GET: Data error")
# store value in new key
			newKey = uuid.uuid4().hex[0:8]
			while ( r.set(newKey, value, nx=True) is None ):
				newKey = uuid.uuid4().hex[0:8]
# delete old key
			if ( key != conf["masterKey"] ):
				r.delete(key)
# return value and the new key
			data[2]=newKey
			logging.info(str(time.time()) + ":  " + str(data)) #T2
			return json.dumps(data)
		else:
			logging.warning(str(time.time()) + ": The key does not exists in the database")
			abort(404, "GET: The key does not exists in the database")
##########
# POST
##########
	elif request.method == 'POST':
		data=request.get_data()
		logging.info(str(time.time()) + ": " + "POST " + request.remote_addr + ' ' + key + ' -> ' + str(data, 'UTF-8')) #T3
		if ( r.set(key,data,xx=True) is None ):
			logging.warning(str(time.time()) + ": The key does not exists in the database")
			abort(409, "POST: The key does not exists in the database")
		return data
##########
# PUT
##########	
	elif request.method == 'PUT':
		data=request.get_data()
		logging.info(str(time.time()) + ": " + "PUT " + request.remote_addr + ' ' + key + ' -> ' + str(data, 'UTF-8'))
		if ( r.set(key,data,nx=True) is None ):
			logging.warning(str(time.time()) + ": The key already exists in the database")
			abort(409, "PUT: The key already exists in the database")
		return data
##########
# HEAD
##########
	if request.method == 'HEAD':
		logging.info(str(time.time()) + ": " + "HEAD " + request.remote_addr + ' ' + key)
# get value as a JSON string
		value = r.get(key)
		if ( value is not None ):
			logging.info(str(time.time()) + ":  key found")
# no entity and no key swapping, just return success (key found)
			return ('',200)
		else:
			logging.warning(str(time.time()) + ": The key does not exists in the database")
			abort(404, "HEAD: The key does not exists in the database")
	else:		
		logging.error("Only GET, POST, PUT and HEAD methods are accepted on this route")
		return abort(405,"Only GET, POST, PUT and HEAD methods are accepted on this route")

if __name__ == '__main__':
   app.run()
