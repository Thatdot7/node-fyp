import RPi.GPIO as GPIO
import sys

# Assigns which GPIO pins controls the plugs
# The pin numbers control plug 1,2,3,4 respectively
pin_translate = [3,5,7,11]


def write(pins):
    # Writes the states of multiple plugs at once
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    for index in range(len(pins)):
        pin = pin_translate[index]
        GPIO.setup(pin, GPIO.OUT)
        if pins[index] == "1":
            GPIO.output(pin, GPIO.HIGH)
        elif pins[index] == "0":
            GPIO.output(pin, GPIO.LOW)

def read():
    # Reads the states of the plugs and returns it
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

    print "%s%s%s%s" %(plug1, plug2, plug3, plug4)
    return "%s%s%s%s" %(plug1, plug2, plug3, plug4)

if __name__ == "__main__":

    if not sys.argv[1:]:
        read()
    else:
        write(sys.argv[1])
