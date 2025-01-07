import time
import RPi.GPIO as GPIO

def init():
    GPIO.setmode(GPIO.BCM)  # choose BCM mode
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.OUT)  # set GPIO 18 as output


def beep(ontime, offtime, repeatnum):
    for cnt in range(repeatnum):
        GPIO.output(18, 1)
        time.sleep(ontime)
        GPIO.output(18, 0)
        time.sleep(offtime)