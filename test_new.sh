#!/bin/bash

if [ $# -eq 0 ] 
then
	echo "Serve la chiave come parametro"
	exit 1
fi

curl -v 127.0.0.1:5000/new/$1
