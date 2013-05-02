import RPi.GPIO as GPIO
import sys

pin_translate = [3,5,7,11]

def write(pins):
    for index in range(len(pins)):
        pin = pin_translate[index]
        GPIO.setup(pin, GPIO.OUT)
        if pins[index] == "1":
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

def read():
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
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    if not sys.argv[1:]:
        read()
    else:
        write(sys.argv[1])
