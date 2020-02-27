#!/home/pi/badge/bin/python
import os
import time
import board
import neopixel
import random
import json
import bluetooth
from bluetooth.ble import DiscoveryService



class BlueFinder():
    def __init__(self):
        self._numpix = 64  # Number of NeoPixels
        self._pixpin = board.D18  # Pin where NeoPixels are connected
        self._strip = neopixel.NeoPixel(self._pixpin, self._numpix, brightness=0.009, auto_write=False)
        self._default_dir = "/home/pi/badge/"
        self._ball_json = "{}balls.json".format(self._default_dir)
        self._mac_vendors_json = "{}macaddress_rpi.json".format(self._default_dir)
        with open(self._mac_vendors_json, 'r') as f:
            self._mac_vendors = json.load(f)
        self._black = (0,0,0)
        self._red = (255, 0, 0)
        self._green = (0, 255, 0)
        self._blue = (0, 0, 255)
        self._yellow = (255,255,0)
        self._teal = (0,255,255)
        self._white = (255,255,255)
        self._orange = (255, 165, 0)

        self._colors = [
            self._black,
            self._red,
            self._green,
            self._blue,
            self._yellow,
            self._teal,
            self._white,
            self._orange
        ]
        self._default_color = self._green
        self._strip.fill(self._default_color)
        self._pixel_colors = {}
        for n in range(0,self._numpix):
            self._pixel_colors.update({n:self._default_color})
        self._balls = {}
        if os.path.exists(self._ball_json):
            try:
                with open(self._ball_json,'r') as f:
                    self._balls = json.load(f)
                for k,v in self._balls.items():
                    self._set_pixel_color(k,v,ball=True,initial=True)
            except:
                os.remove(self._ball_json)
        self._strip.show()

    def _set_pixel_color(self,i,c,ball=False,initial=False):
        if isinstance(i, str):
            i = int(i)
        if isinstance(c,list):
            c = tuple(c)
        print(i,c)
        self._strip[i] = c
        if not initial:
            self._pixel_colors[i] = c
        if ball:
            if not initial:
                self._balls.update({i:c})
            with open(self._ball_json, 'w') as f:
                print("and here")
                json.dump(self._balls,f,indent=4)
        self._strip.show()

    def _get_pixel_color(self,i):
        return self._pixel_colors.get(i)

    def run_radar_scan(self):
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
                if i not in self._balls.keys():
                    self._set_pixel_color(i,self._yellow)
            self._strip.show()
            time.sleep(1)
            for i in cycle:
                if i not in self._balls.keys():
                    self._set_pixel_color(i,self._default_color)
            self._strip.show()
            time.sleep(1)

    def run_radar_red(self):
        first = [27,28,35,36]
        second = [18,19,20,21,26,29,34,37,42,43,44,45]
        third = [9,10,11,12,13,14,17,22,25,30,33,38,41,46,49,50,51,52,53,54]
        fourth = [0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63]
        cycles = [first,second,third,fourth]
        for cycle in cycles:
            for i in cycle:
                if i not in self._balls.keys():
                    self._set_pixel_color(i,self._red)
            self._strip.show()
            time.sleep(1)
            for i in cycle:
                if i not in self._balls.keys():
                    self._set_pixel_color(i,self._default_color)
            self._strip.show()
            time.sleep(1)

    def ball_locate(self):
        num = random.randint(0,63)
        if len(self._balls.keys()) == 7:
            return
        if num in self._balls.keys():
            self.ball_locate()
        self._set_pixel_color(num,self._orange,ball=True)

    def done_check(self):
        if len(self._balls.keys()) == 7:
            return True
        return False

    def blink_balls(self):
        for i in self._balls.keys():
            self._set_pixel_color(i,self._default_color,ball=False,initial=True)
        self._strip.show()
        time.sleep(1)
        for i in self._balls.keys():
            self._set_pixel_color(i,self._orange,ball=False,initial=True)
        self._strip.show()
        time.sleep(1)

    def get_mac_vendor(self, macaddr):
        macaddr = ":".join(macaddr.split(":")[0:3])
        mac_ven = self._mac_vendors.get(macaddr)
        if mac_ven:
            return mac_ven
        return

    def find_devices(self):
        mac_addrs = []
        nearby_devices = bluetooth.discover_devices()
        if nearby_devices:
            be_addrs = [addr for addr, name in nearby_devices]
            if be_addrs:
                mac_addrs.extend(be_addrs)
        service = DiscoveryService()
        devices = service.discover(2)
        be_le_addrs =  devices.keys()
        if be_le_addrs:
            mac_addrs.extend(be_le_addrs)
        if mac_addrs:
            mac_addrs = [self.get_mac_vendor(mac_addr) for mac_addr in mac_addrs if self.get_mac_vendor(mac_addr)]
        return mac_addrs


def main():
    obj = BlueFinder()
    while True:
        if obj.done_check():
            obj.blink_balls()
        else:
            obj.ball_locate()
            obj.run_radar_scan()

if __name__ == '__main__':
    main()
