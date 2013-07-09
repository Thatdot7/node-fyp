import subprocess
from configobj import ConfigObj

def update():
	config = ConfigObj('/home/pi/node-fyp/config/general.ini')
	if config['range_extension']['enable']:
		subprocess.call('service hostapd restart', shell=True)
		subprocess.call('service udhcpd restart', shell=True)
	else:
		subprocess.call('service hostapd stop', shell=True)
		subprocess.call('service udhcpd stop', shell=True)


if __name__ == "__main__":
	update()
