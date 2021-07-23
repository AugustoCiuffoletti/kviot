#!/bin/bash

key="45678925"
value="[ false, \"{'id': '$1', 'tref': 18, 'age': 0}\"]"
#TCPADDR=127.0.0.1
#TCPADDR=127.0.0.1:5000
TCPADDR=192.168.113.181
TEMPFILE=$(mktemp /tmp/kviotXXXXX)
CURLOPT="--output $TEMPFILE --silent --write-out %{http_code}"

# Questa è la parte dell'operatore

while [ $(curl $CURLOPT -X PUT -H "Content-Type: application/json" -d "$value" $TCPADDR/$key) != 200 ]
do 
	echo "Key conflict ($key): retry"
	sleep 1
	key=`openssl rand -hex 4`
done


# Questa è la parte del mote

while true 
do
	# Qui sarebbe meglio un loop se la chiave è già occupata
	if [ $(curl $CURLOPT $TCPADDR/$key) == 200 ]
	then
		cat $TEMPFILE
		key=$(jq  '.[2]' $TEMPFILE | tr -d '"')
	else
		echo fail
	fi

	encode=$(jq  '.[0]' $TEMPFILE)
	parameters=$(jq  '.[1]' $TEMPFILE)
# Qui decodifica e modifica i parametri (sarebbe meglio comunque un URLencode)	
	age=$(echo $parameters | tr -d '"' | tr "\'" "\"" | jq '.age + 1')
	id=$(echo $parameters | tr -d '"' | tr "\'" "\"" | jq '.id' | tr -d '"')
	tref=$(echo $parameters | tr -d '"' | tr "\'" "\"" | jq '.tref')
	parameters="\"{'id': '$id', 'tref': $tref, 'age': $age}\""
echo $parameters
	value="[ $encode, $parameters ]"
	

	if [ $(curl $CURLOPT -X POST -d "$value" $TCPADDR/$key) ]
	then
		echo Looping
	else
		echo fail
	fi
	sleep 1
done
