import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_ADS1x15
import adafruit_ahtx0
import board
import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

# Define the font size and style
from PIL import ImageFont
font = ImageFont.load_default(16)
	
dustPin = 2;
ledPin = 4;
Tsampling = 280;
Tdelta = 40;
Tsleep = 9680;
outVo = 0.0;
sigVolt = 0.0;
dustLevel = 0.0;
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115(busnum=2)

# Initialize the I2C serial interface
serial = i2c(port=1, address=0x3C)  # Use the correct I2C address (0x3C or 0x3D) for your OLED display
device = ssd1306(serial, width=128, height=64)  # Set the width and height according to your display's specifications

i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)
# Create a function to display text on the OLED screen
def display_text(text, text2, text3):
    with canvas(device) as draw:
        draw.text((10, 0), text, font=font, fill="white")
        draw.text((10, 20), text2,font=font, fill="white")
        draw.text((10, 40), text3, font=font, fill="white")
         
# Initialize the ADC
adc = Adafruit_ADS1x15.ADS1115(busnum=2)

GAIN = 1  # Set the gain (1 for +/-4.096V)
dustPin = 2;
ledPin = 4;
Tsampling = 280;
Tdelta = 40;
Tsleep = 9680;
outVo = 0.0;
sigVolt = 0.0;
dustLevel = 0.0;


try:
    while True:
        GPIO.output(ledPin, GPIO.LOW)
    
        time.sleep(Tsampling/1000000)

        outVo = adc.read_adc(dustPin, gain=GAIN);

        time.sleep(Tdelta/1000000)

        GPIO.output(ledPin, GPIO.HIGH)
    
        time.sleep(Tsleep/1000000)

        sigVolt = outVo * (4.096/32767.0);

        dustLevel = .1-0.17 * sigVolt;

        # Read all the ADC channel values in a list.
        Smoke_val = 0
        CO_val = 0

        # Defining constants
        r0 = 0.38
        ppm = .0

        # The read_adc function will get the value of the specified channel (0-7).
        Smoke_val = adc.read_adc(1, gain=GAIN)*(4.096/32767.0)
        CO_val = adc.read_adc(0, gain=GAIN)

        # Calculating Smoke and CO values
        sensor_volt = CO_val*(4.096/32767.0)

        if sensor_volt == 0:
            RS_gas = 0
        else:
            RS_gas = (4.096 - sensor_volt)/sensor_volt
        
        CO_ratio = RS_gas/r0
        ppm = 47.947*sensor_volt - 79.73501
        
        temperature =  sensor.temperature
        humidity = sensor.relative_humidity

        print("\nTemperature: {:0.1f} C".format(temperature))
        print("Humidity: {:.1f}".format(humidity))
        # Print the ADC values.
        print("Dust Density Level (in ug/m^3): {:.5f}".format(dustLevel));
        print('CO value (Rs\Ro): {:.3f}'.format(CO_ratio))
        print('Smoke value (in V): {:.3f}'.format(Smoke_val))
        #print('Smoke value: {:.3f}'.format(ppm))
        display_text(f"MQ7: %0.2f" % CO_ratio, f"MQ135: %0.2f" % Smoke_val , f"Dust: %0.5f" % dustLevel)
        time.sleep(1)
        display_text(f"Temp: %0.1f C" % sensor.temperature, f"Humi: %0.1f %%" % sensor.relative_humidity, f"")
        time.sleep(1)  # You can adjust the sampling interval
except KeyboardInterrupt:
    pass
