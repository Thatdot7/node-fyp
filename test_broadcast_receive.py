import socket, select
import json
import netifaces
import subprocess

# Socket Setup
# Attributes of UDP, non-blocking, reusable ports and broadcast
# Listen on port 1234 from anywhere
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
s.bind(('', 1234))
s.setblocking(0)

return_msg = [{ "Zone": "Bedroom 1",
		"Device" : "Smart Powerboard"
		}]


# Function to get the details of the IP address information from each interface
def ip_addressv4():
	list = []
	for interface in netifaces.interfaces():
		try:
			details = netifaces.ifaddresses(interface)[2][0]
			details['addr'] = details['addr'].split('.')
			details['netmask'] = details['netmask'].split('.')
			list.append(details)
		except:
			continue
	
	return list

# Start the infinite loop to wait for packets to come in
while True:

	# When the packet is ready to be receive, receive and extract the message
	# and source address of packet
	result = select.select([s],[],[])
	(msg, address) = result[0][0].recvfrom(1024)

	# Discard all packets that come from this computer
	self_address_list = subprocess.check_output("hostname -I", shell=True).split(' ')
	if address[0] in self_address_list:
		continue
	
	print msg
	print address

	# Find which network the packet came from then broadcast it to all the other networks
	address_array = address[0].split('.')
	broadcast_list = []
	for links in ip_addressv4():
		for ip_block in range(4):
			network_array = int(links['addr'][ip_block]) & int(links['netmask'][ip_block])
			compared_array = int(links['netmask'][ip_block]) & int(address_array[ip_block])
			if compared_array != network_array:
				try:
					broadcast_list.append(links['broadcast'])
				except:
					continue

	
	print broadcast_list

	# Check if there is a "source" field. If there isn't, put on in
	# then send the device information to the relevant address
	if msg,get('source'):
		s.sendto(json.dumps(return_msg), source)
	else:
		msg['source'] = address
		s.sendto(json.dumps(return_msg), address)

	# Broadcast the original message to all other networks
	for broadcast in broadcast_list:
		s.sendto(json.dumps(msg, (broadcast, 1234))
