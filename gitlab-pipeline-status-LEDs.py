import time
import board
import neopixel
import requests
import json


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 4

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

# brightness=0.2 ~10mA and brightness=1 ~62mA with rainbow effect and 5 NeoPixels
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)

url = "https://gitlab.com/api/v4/projects/1382/pipelines?per_page=4"
token = ""

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

def map_pipeline_to_status(pipeline):
    return pipeline["status"]


def fetch_pipelines():
    response = requests.get(url, headers = { "PRIVATE-TOKEN": token})
    statuses = list(map(map_pipeline_to_status, response.json()))

    return statuses


def map_status_to_rgb(status):
    if status in ("created", "waiting_for_resource", "preparing", "pending"):
        return BLUE
    elif status in ("running"):
        return YELLOW
    elif status in ("failed"):
        return RED
    elif status in ("canceled", "skipped", "manual", "scheduled"):
        return PURPLE
    elif status in ("success"):
        return GREEN


if __name__ == '__main__':

    while True:
        pipeline_statuses = fetch_pipelines()
        led_colors = list(map(map_status_to_rgb, pipeline_statuses))

        for i in range(len(led_colors)):
            pixels[i] = led_colors[i]

        pixels.show()
        time.sleep(10)

