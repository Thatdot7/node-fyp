#!/bin/bash

port=49152
addr=0

for ((a=1; a<= 254; a++))
do
	let port++
	let addr++
	echo "sudo iptables -t nat -A PREROUTING -p tcp -i wlan1 --dport $port -j DNAT --to 192.168.7.$addr:80"
	sudo iptables -t nat -A PREROUTING -p tcp -i wlan1 --dport $port -j DNAT --to 192.168.7.$addr:80
done
echo; echo

exit 0
