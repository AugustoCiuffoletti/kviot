#/bin/bash

if [ $# -eq 0 ] 
then
	echo "Serve la chiave come parametro"
	exit 1
fi

for i in {1..400}
do
	{
		ts0=`date +%s%N`
		echo "$i" | curl --silent --data-binary @- 192.168.113.155/value/$1 > /dev/null
		curl --silent 192.168.113.155/value/$1 > /dev/null
		ts1=`date +%s%N`
		expr \( $ts1 - $ts0 \) / 1000000
	} & # Qui aggiungere & per mandare concorrenti
done
