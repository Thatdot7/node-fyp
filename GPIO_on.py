import RPi.GPIO as GPIO
import sys
from configobj import  ConfigObj

#####################################################################################################################
# GPIO_on
#
# This script is only meant to push a particular pin in the GPIO to its HIGH state.
# Before use, please read about the particular functions of each GPIO pin to ensure that it is usable for you
#####################################################################################################################

def run_script(pins):
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)

	config_file = ConfigObj("/home/pi/node-fyp/config/general.ini")
	pin_translate = config_file["pin_settings"]["outlets"]

	pin = pin_translate[int(pins)-1]
	GPIO.setup(int(pin), GPIO.OUT)
	GPIO.output(int(pin), GPIO.HIGH)

	print "Pin " + str(pin) + " is now high"

if __name__ == "__main__":
	run_script(sys.argv[1])

