#/bin/bash

if [ $# -eq 0 ] 
then
	echo "Serve la chiave come parametro"
	exit 1
fi

echo -n "data> "
curl -v -X POST --data-binary @- 127.0.0.1:5000/value/$1
