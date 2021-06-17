#!/bin/bash

key="45678925"
value="[ false, \"{'id': '$1', 'tref': 18}\"]"
DOMAIN=127.0.0.1:5000
TEMPFILE=""
CURLOPT="--output /tmp/temp --silent --write-out %{http_code}"

# Questa è la parte dell'operatore

while [ $(curl $CURLOPT -X PUT -H "Content-Type: application/json" -d "$value" 127.0.0.1/$key) != 200 ]
do 
	echo "Key conflict ($key): retry"
	sleep 1
	key=`openssl rand -hex 4`
done


# Questa è la parte del mote

while true 
do
	# Qui sarebbe meglio un loop se la chiave è già occupata
	if [ $(curl $CURLOPT 127.0.0.1:5000/$key) == 200 ]
	then
		cat /tmp/temp
		key=$(jq  '.[2]' /tmp/temp | tr -d '"')
	else
		echo fail
	fi

# Qui costruire un nuovo "value"

	if [ $(curl $CURLOPT -X POST -d "$value" 127.0.0.1:5000/$key) ]
	then
		echo Looping
	else
		echo fail
	fi
	sleep 1
done
