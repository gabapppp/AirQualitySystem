import redis
import socket
from pymongo import MongoClient
from datetime import datetime
import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_ADS1x15
import board
import adafruit_ahtx0
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306


# Define the font size and style
from PIL import ImageFont
font = ImageFont.load_default(16)
# Initialize DB
uri = "mongodb+srv://gabap:FmJPMHijB74BsuZ6@cluster0.widcuv7.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(uri)
    db = client.database
    connected = True
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

dustPin = 2;
ledPin = 4;
Tsampling = 280;
Tdelta = 40;
Tsleep = 9680;
outVo = 0.0;
sigVolt = 0.0;
dustLevel = 0.0;
CO_ppm = 0.0;
CO2_ppm = 0.0;
temperature = 1.0;
humidity = 0.0;
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

sensor = adafruit_ahtx0.AHTx0(board.I2C())


# Create a function to display text on the OLED screen
def display_text(text, text2, text3):
    with canvas(device) as draw:
        draw.text((10, 0), text, font=font, fill="white")
        draw.text((10, 20), text2,font=font, fill="white")
        draw.text((10, 40), text3, font=font, fill="white")

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1
"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

try:
    while True:
        GPIO.output(ledPin, GPIO.LOW)
        time.sleep(Tsampling/1000000)
        outVo = adc.read_adc(dustPin, gain=GAIN)*(5.0/10581.0);
        time.sleep(Tdelta/1000000)
        GPIO.output(ledPin, GPIO.HIGH)
        time.sleep(Tsleep/1000000)
        dustLevel = (0.17 * outVo - 0.1)*1000.0;
        if (dustLevel< 0):
            dustLevel = 0.00;
        # Read all the ADC channel values in a list.
        Smoke_val = 0
        CO_val = 0
        # Defining constants
        r0 = 76.63
        RL = 10.0
        # The read_adc function will get the value of the specified channel (0-7).
        Smoke_val = adc.read_adc(1, gain=GAIN)
        CO_val = adc.read_adc(0, gain=GAIN)
        # Calculating Smoke and CO values
        Smoke_sensor_volt = Smoke_val*(5.0/21470.0)
        CO_sensor_volt = CO_val*(5.0/5470.0)
        #RS_Smoke = ((1023.0/Smoke_val*5.0-1.0)*RL)/0.52295515
        RS_Smoke =(5.0*RL-(RL*Smoke_sensor_volt))/Smoke_sensor_volt
        CO_ratio = (5.0-CO_sensor_volt)/CO_sensor_volt
        #CO2_ppm = (146.15*(2.868-RS_Smoke/r0* 0.3611)+10.0)
        CO2_ppm = 116.6020682*pow(RS_Smoke/r0, -2.769034857)
        CO_ppm = 19.32*pow(CO_ratio,-0.64)
        if(CO_ppm > 1000):
            CO_ppm = 1000;
        #CO_ppm = 47.947*CO_sensor_volt - 79.73501

        CO_ppm = round(CO_ppm, 2)
        CO2_ppm = round(CO2_ppm, 2)
        dustLevel = round(dustLevel, 2)
        temperature =  round(sensor.temperature, 2)
        humidity = round(sensor.relative_humidity, 2)

        IPAddr = get_local_ip()
        
        if(connected == True):
            data = {
            "pm25": dustLevel,
            "mq7": CO_ppm,
            "mq135": CO2_ppm,
            "temperature": temperature,
            "humidity": humidity,
            "time": get_current_datetime()
            }
            db.sensordata.insert_one(data);

        redis_db.set("pm25", str(dustLevel))
        redis_db.set("mq7", str(CO_ppm))
        redis_db.set("mq135", str(CO2_ppm))
        redis_db.set("temperature", str(temperature))
        redis_db.set("humidity", str(humidity))
        
        display_text(f"CO: %0.1f" % CO_ppm, f"CO2: %0.1f" % CO2_ppm , f"Dust: %0.1f" % dustLevel)
        time.sleep(2)
        display_text(f"Temp: %0.1f °C" % temperature, f"Humi: %0.1f %%" % humidity, f"")
        time.sleep(2)  # You can adjust the sampling interval
        display_text(f"Group 12", f"IP:", f"%s" % IPAddr)
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
    pass