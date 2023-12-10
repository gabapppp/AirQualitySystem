import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
 
# Define the font size and style
from PIL import ImageFont
font = ImageFont.load_default(16)
 
# Create an ADS1115 object
ads = ADS.ADS1115(busio.I2C(board.SCL, board.SDA))
 
# Define the analog input channels
channel0 = AnalogIn(ads, ADS.P0)
channel1 = AnalogIn(ads, ADS.P1)
channel2 = AnalogIn(ads, ADS.P2)
channel3 = AnalogIn(ads, ADS.P3)

# Initialize the I2C serial interface
serial = i2c(port=1, address=0x3C)  # Use the correct I2C address (0x3C or 0x3D) for your OLED display
device = ssd1306(serial, width=128, height=64)  # Set the width and height according to your display's specifications

# Create a function to display text on the OLED screen
def display_text(text, text2, text3):
    with canvas(device) as draw:
        draw.text((10, 0), text, font=font, fill="white")
        draw.text((10, 20), text2,font=font, fill="white")
        draw.text((10, 40), text3, font=font, fill="white")
 
# Loop to read the analog inputs continuously
try:
    while True:
        print("Analog Value 0: ", channel0.value, "Voltage 0: ", channel0.voltage)
        print("Analog Value 1: ", channel1.value, "Voltage 1: ", channel1.voltage)
        print("Analog Value 2: ", channel2.value, "Voltage 2: ", channel2.voltage)
        print("Analog Value 3: ", channel3.value, "Voltage 3: ", channel3.voltage)
        
        # Delay for 1 second
        time.sleep(1)

        #time.sleep(2)
except KeyboardInterrupt:
    pass
