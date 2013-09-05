import RPi.GPIO as GPIO
import sys
from configobj import ConfigObj


def write(pins):
    # Writes the states of multiple plugs at once
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    config_file = ConfigObj("/home/pi/node-fyp/config/general.ini")
    pin_translate = config_file["pin_settings"]["outlets"]

    for index in range(len(pins)):
        pin = int(pin_translate[index])
        GPIO.setup(pin, GPIO.OUT)
        if pins[index] == "1":
            GPIO.output(pin, GPIO.HIGH)
        elif pins[index] == "0":
            GPIO.output(pin, GPIO.LOW)

def read():
    # Reads the states of the plugs and returns it
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    config_file = ConfigObj("/home/pi/node-fyp/config/general.ini")
    read_pins = config_file["pin_settings"]["read_pins"]

    for pin in read_pins:
        GPIO.setup(int(pin), GPIO.IN)

    plug1 = str(GPIO.input(int(read_pins[0])))
    plug2 = str(GPIO.input(int(read_pins[1])))
    plug3 = str(GPIO.input(int(read_pins[2])))
    plug4 = str(GPIO.input(int(read_pins[3])))

    print "%s%s%s%s" %(plug1, plug2, plug3, plug4)
    return "%s%s%s%s" %(plug1, plug2, plug3, plug4)

if __name__ == "__main__":

    if not sys.argv[1:]:
        read()
    else:
        write(sys.argv[1])
