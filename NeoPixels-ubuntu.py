# Simple test for NeoPixels on Raspberry Pi
import time
from rpi_ws281x import *

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = 18

# The number of NeoPixels
num_pixels = 1

# brightness=0.2 ~10mA and brightness=1 ~62mA with rainbow effect and 5 NeoPixels
intensity = 1.0
pixels = Adafruit_NeoPixel(num_pixels, pixel_pin)
pixels.begin()

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) #if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            rgb = wheel(pixel_index & 255)
            set_color(i, rgb)
        pixels.show()
        time.sleep(wait)


def fill(rgb):
    for i in range(pixels.numPixels()):
        set_color(i, rgb)

def set_color(i, rgb):
    r = int(rgb[0] * intensity)
    g = int(rgb[1] * intensity)
    b = int(rgb[2] * intensity)
    pixels.setPixelColorRGB(i, r, g, b)

def cycle(wait):
    fill((255, 0, 0))
    pixels.show()
    time.sleep(wait)

    fill((0, 255, 0))
    pixels.show()
    time.sleep(wait)

    fill((0, 0, 255))
    pixels.show()
    time.sleep(wait)


while True:
    try:
        rainbow_cycle(0.005)  # rainbow cycle with 1ms delay per step
   #    cycle(0.5) # cycle between RGB
    except:
        fill((0,0,0))
