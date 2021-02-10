##
# Raspberry Pi 4
# Author: csbc
# Description: Turns on the individual colors of an RGB LED
# Prerequisites:
# 1) Add the user to the gpio group:
#      sudo usermod -a -G gpio pi
# 2) Make sure that you double check the connections between the the GPIO and RGB LED.
#    Beware of the difference between GPIO.BOARD and GPIO.BCM
#
##

import RPi.GPIO as GPIO
import time
import math
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def toggle(led):
    if (GPIO.input(led)):
        GPIO.output(led, GPIO.LOW)
    else:
        GPIO.output(led, GPIO.HIGH)
        
def bool_to_pin(b):
    if b:
        return GPIO.HIGH
    else:
        return GPIO.LOW
        
def turn_off_rgb(leds):
    for led in leds:
        GPIO.output(led, GPIO.LOW)

def set_rgb(integer, leds):
    # No. of states: 2^3 = 8
    # Allowed states: 0, 1, .., 7
    
    if not (0 <= integer and integer <= 7):
        raise Exception("Illegal parameter: state. Must be within [0, 1, .., 7]")
    
    binary_state = convert_to_bin(integer)
    print(binary_state)
    
    turn_off_rgb(leds)
    
    # Set the intended rgb
    # blue is lowest value (1)
    # red is highest value (7)
    for i in range(len(binary_state)):
        index = len(leds)-i-1
        index2 = len(binary_state)-i-1
        GPIO.output(leds[index], bool_to_pin(binary_state[index2]))

def init_bin_arr(s):
# Prepares an array with enough space to store the provided integer value in binary form
    if s == 0 or s == 1:
        return [False]
    else:
        return [False] * math.ceil((math.log2(s+1)))

def reverse_array(arr):
    return arr[::-1]

def convert_to_bin_arr(s, p, bin_arr):
    if s == 0:
        return reverse_array(bin_arr) # Left-most bit is most significant bit
    
    if (s / (math.pow(2, p))) >= 1:
        bin_arr[p] = True
        s = (s - math.pow(2, p))
    else:
        bin_arr[p] = False
        
    return convert_to_bin_arr(s, p-1, bin_arr)
    
def convert_to_bin(integer):
    integer_to_convert_to_binary = integer
    bin_arr = init_bin_arr(integer_to_convert_to_binary)
    potens = len(bin_arr) - 1
    return convert_to_bin_arr(integer_to_convert_to_binary, potens, bin_arr)

def init_rgb_led():
    r = 29
    g = 33
    b = 37
    leds = [r, g, b]

    GPIO.setup(r, GPIO.OUT)
    GPIO.setup(g, GPIO.OUT)
    GPIO.setup(b, GPIO.OUT)
    GPIO.output(r, GPIO.LOW)
    GPIO.output(g, GPIO.LOW)
    GPIO.output(b, GPIO.LOW)
    
    return leds


rgb_led = init_rgb_led()

while True:
    for i in range(1,8):
        set_rgb(i, rgb_led)
        time.sleep(0.2)