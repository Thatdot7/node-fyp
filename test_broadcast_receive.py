import socket, select
import json

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
s.bind(('', 1234))
s.setblocking(0)

while True:
	result = select.select([s],[],[])
	(msg, address) = result[0][0].recvfrom(1024)
	print msg

	return_msg = [{ "Zone": "Bedroom 1",
			"Device" : "Smart Powerboard"
			}]

	s.sendto(json.dumps(return_msg), address)
