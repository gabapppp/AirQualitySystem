import Adafruit_ADS1x15
import time

# Initialize the ADC
adc = Adafruit_ADS1x15.ADS1115(2)
GAIN = 1  # Set the gain (1 for +/-4.096V)

def read_gp2y1010au0f_value():
    gp2y1010au0f_value = adc.read_adc(2, gain=GAIN)
    return gp2y1010au0f_value

try:
    while True:
        gp2y1010au0f_value = read_gp2y1010au0f_value()
        print(f"GP2Y1010AU0F Value: {gp2y1010au0f_value}")
        time.sleep(1)  # You can adjust the sampling interval
except KeyboardInterrupt:
    pass
