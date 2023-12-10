import board
import adafruit_ahtx0
import time

i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)
while True:
	print("\nTemperature: %0.1f C" % sensor.temperature)
	print("Humidity: %0.1f %%" % sensor.relative_humidity)
	time.sleep(1)
