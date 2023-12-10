import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import time

# Initialize the ADC
adc = Adafruit_ADS1x15.ADS1115(busnum=2)
GAIN = 1  # Set the gain (1 for +/-4.096V)

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)


def read_gp2y1010au0f_value():
    gp2y1010au0f_value = adc.read_adc(2, gain=GAIN)
    return gp2y1010au0f_value


while True:
        GPIO.output(4, 1)
        time.sleep(0.00028)
        GPIO.output(4, 0)
        time.sleep(0.00004)
        gp2y1010au0f_value = read_gp2y1010au0f_value()
        print(f"GP2Y1010AU0F Value: {gp2y1010au0f_value}")
        time.sleep(0.00968)

try:
    while True:
        GPIO.output(17, 1)
        time.sleep(0.00028)
        GPIO.output(17, 0)
        time.sleep(0.00004)
        gp2y1010au0f_value = read_gp2y1010au0f_value()
        print(f"GP2Y1010AU0F Value: {gp2y1010au0f_value}")
except KeyboardInterrupt:
    pass

