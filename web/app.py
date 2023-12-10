from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
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
         
sensor = adafruit_ahtx0.AHTx0(i2c)

dustPin = 3;
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
adc = Adafruit_ADS1x15.ADS1115()

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
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZUCGiYmt_H3~ZGJ'
socketio = SocketIO(app, cors_allowed_origins='*')
"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""

def background_thread():
    print("Generating random sensor values")
    while True:
        GPIO.output(ledPin, GPIO.LOW)
    
        time.sleep(Tsampling/1000000)

        outVo = adc.read_adc(dustPin, gain=GAIN)*(5.0/7081.0);

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
        ppm = .0

        RL = 10.0

        # The read_adc function will get the value of the specified channel (0-7).
        Smoke_val = adc.read_adc(1, gain=GAIN)
        CO_val = adc.read_adc(0, gain=GAIN)

        # Calculating Smoke and CO values
        #Smoke_sensor_volt = Smoke_val*(5.0/24470.0)
        CO_sensor_volt = CO_val*(5.0/29870.0)

        RS_Smoke = ((1023.0/Smoke_val*5.0-1.0)*RL)/0.52295515
        #RS_Smoke =(5.0*RL-(RL*Smoke_sensor_volt))/Smoke_sensor_volt
        CO_ratio = (5.0-CO_sensor_volt)/CO_sensor_volt
        #CO2_ppm = (146.15*(2.868-RS_Smoke/r0* 0.3611)+10.0)
        CO2_ppm = 116.6020682*pow(RS_Smoke/r0, -2.769034857)
        CO_ppm = 19.32*pow(CO_ratio,-0.64)
        #ppm = 47.947*CO_sensor_volt - 79.73501
        


        temperature =  sensor.temperature
        humidity = sensor.relative_humidity
        
        print("\nTemperature: {:0.1f} C".format(temperature))
        print("Humidity: {:.1f}".format(humidity))
        # Print the ADC values.
        print("Dust Density Level (in ug/m^3): {:.5f}".format(dustLevel));
        print('CO ppm: {:.2f}'.format(CO_ppm))
        print('Smoke(CO2) ppm: {:.2f}'.format(CO2_ppm))
        
        socketio.emit('updateSensorData', {
            "pm25": dustLevel,
            "mq7": CO2_ppm,
            "mq135": CO_ppm,
            "temperature": temperature,
            "humidity": humidity,
            "date": get_current_datetime()})
        
        display_text(f"CO: %0.1f" % CO_ppm, f"CO2: %0.1f" % CO2_ppm , f"Dust: %0.1f" % dustLevel)
        time.sleep(0.5)
        display_text(f"Temp: %0.1f C" % temperature, f"Humi: %0.1f %%" % humidity, f"")
        time.sleep(0.5)  # You can adjust the sampling interval

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/mq135")
def get_mq135_list():
    
    return Response({"None: None"})

@app.route("/pm25")
def get_pm25_list():
    return Response({})


"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)