from flask import Flask, request, abort
from redis.client import Redis

app = Flask(__name__)
r = Redis()

@app.route('/value/<key>',methods = ['POST', 'GET'])
def KVsvc(key):
	if request.method == 'GET':
		if ( r.exists(key) ):
			return r.get(key)
		else:
			abort(404, "GET: The key does not exists in the database")
	elif request.method == 'POST':
		data=request.get_data()
		print(data)
		print(key)
		if ( r.exists(key) ):
			r.set(key,data)
			return data
		else:
			abort(404, "POST: The key does not exists in the database")
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
