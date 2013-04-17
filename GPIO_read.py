import RPi.GPIO as GPIO

def run_script():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)

	GPIO.setup(21, GPIO.IN)
	GPIO.setup(22, GPIO.IN)
	GPIO.setup(23, GPIO.IN)
	GPIO.setup(24, GPIO.IN)

	plug1 = str(GPIO.input(21))
	plug2 = str(GPIO.input(22))
	plug3 = str(GPIO.input(23))
	plug4 = str(GPIO.input(24))

	return "%s%s%s%s" %(plug1, plug2, plug3, plug4)

if __name__ == "__main__":
	run_script()
