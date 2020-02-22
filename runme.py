#!/home/pi/badge/bin/python
#import board
#import neopixel
#pixels = neopixel.NeoPixel(board.D18, 64, brightness=0.004)
#pixels.fill((255,0,0))
# pip3 install rpi_ws281x adafruit-circuitpython-neopixel

import time
import board
import neopixel
try:
    import urandom as random
except ImportError:
    import random

numpix = 64  # Number of NeoPixels
pixpin = board.D18  # Pin where NeoPixels are connected
strip = neopixel.NeoPixel(pixpin, numpix, brightness=0.004, auto_write=False)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255,255,0)
teal = (0,255,255)
white = (255,255,255)

colors = [
    red,
    green,
    blue,
    yellow,
    teal,
    white
]

strip.fill(green)
pixel_colors = {}
balls = {}
for n in range(0,numpix):
    pixel_colors.update({n:green})
strip.show()

def set_pixel_color(i,c,ball=False):
    strip[i] = c
    pixel_colors[i] = c
    if ball:
        balls.update({i:c})
    strip.show()

def get_pixel_color(i):
    return pixel_colors.get(i)

def run_radar_scan():
    first = [4,12,20,28]
    second = [28,21,14,7]
    third = [28,29,30,31]
    fourth = [36,45,54,63]
    fifth = [36,44,52,60]
    sixth = [35,42,49,56]
    seventh = [35,34,33,32]
    eighth = [27,18,9,0]
    nineth = [27,19,11,3]
    cycles = [first,second,third,fourth,fifth,sixth,seventh,eighth,nineth]
    for cycle in cycles:
        for i in cycle:
            strip[i] = yellow
        strip.show()
        time.sleep(1)
        for i in cycle:
            strip[i] = green
        strip.show()
        time.sleep(1)

def run_radar_red():
    first = [27,28,35,36]
    second = [18,19,20,21,26,29,34,37,42,43,44,45]
    third = [9,10,11,12,13,14,17,22,25,30,33,38,41,46,49,50,51,52,53,54]
    fourth = [0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63]
    cycles = [first,second,third,fourth]
    for cycle in cycles:
        for i in cycle:
            strip[i] = red
        strip.show()
        time.sleep(1)
        for i in cycle:
            strip[i] = green
        strip.show()
        time.sleep(1)


while True:
    run_radar_red()



#while True:
#    c = colors[random.randint(0,len(colors)-1)]  # Choose random color index
#    j = random.randint(0, numpix - 1)  # Choose random pixel
#    strip[j] = c # Set pixel to color
#    print("{} : {}".format(c,j))
#    time.sleep(1)
