from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import cv2
# Initialize the I2C serial interface
serial = i2c(port=1, address=0x3C)  # Use the correct I2C address (0x3C or 0x3D) for your OLED display
device = ssd1306(serial, width=128, height=64)  # Set the width and height according to your display's specifications

# Create a function to display text on the OLED screen
def display_text(text):
    with canvas(device) as draw:
        draw.text((10, 10), text, fill="white")

# Call the function with the text you want to display
display_text("Hello, OLED!")

# You can call the function with different text to change what's displayed
while True:
    # Call the function with the text you want to display
    display_text("Hello, OLED!")
    if cv2.waitKey(1) & 0xFF == 27:
            break
