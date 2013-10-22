import subprocess
from configobj import ConfigObj
import GPIO_handler

def update():
	config = ConfigObj('/home/pi/node-fyp/config/general.ini')

	GPIO_handler.write(config['last_state']['plug_state'])
	if config['range_extension']['enable'] == 'true':
		subprocess.call('ifconfig wlan0 ' + config['range_extension']['router'] + ' netmask ' + config['range_extension']['netmask'], shell=True)
		subprocess.call('service isc-dhcp-server restart', shell=True)
		subprocess.call('service hostapd restart', shell=True)
	else:
		subprocess.call('service hostapd stop', shell=True)
		subprocess.call('service udhcpd stop', shell=True)


if __name__ == "__main__":
	update()
