#!/usr/bin/env python3
import os
import time
import json
import random
# 3rd party
import board
import neopixel
import asyncio
from bleak import BleakScanner


class BlueFinder():
    def __init__(self):
        self._numpix = 64  # Number of NeoPixels
        self._pixpin = board.D18  # Pin where NeoPixels are connected
        self._strip = neopixel.NeoPixel(self._pixpin, self._numpix, brightness=0.009, auto_write=False)
        self._default_dir = os.getcwd()
        self._ball_json = os.path.join(self._default_dir, "balls.json")
        self._found_vendors_json = os.path.join(self._default_dir, "found_vendors.json")
        if os.path.exists(self._found_vendors_json):
            with open(self._found_vendors_json, 'r') as f:
                self._found_vendors_list = json.load(f)
        else:
            self._found_vendors_list = []
        self._mac_vendors_json = os.path.join(self._default_dir,"macaddress_rpi.json")
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
            _ = self._pixel_colors.update({n:self._default_color})
        self._balls = {}
        if os.path.exists(self._ball_json):
            try:
                with open(self._ball_json,'r') as f:
                    self._balls = json.load(f)
                for k,v in self._balls.items():
                    _ = self._set_pixel_color(k,v,ball=True,initial=True)
            except:
                os.remove(self._ball_json)
        self._strip.show()

    def _set_pixel_color(self,i,c,ball=False,initial=False):
        if isinstance(i, str):
            i = int(i)
        if isinstance(c,list):
            c = tuple(c)
        self._strip[i] = c
        if not initial:
            self._pixel_colors[i] = c
        if ball:
            if not initial:
                self._balls.update({i:c})
            with open(self._ball_json, 'w') as f:
                json.dump(self._balls,f,indent=4)
        self._strip.show()

    def _get_pixel_color(self,i):
        return self._pixel_colors.get(i)

    def run_radar_scan(self, scan_color=None):
        if not scan_color:
            scan_color = self._white
        first = [27,28,35,36]
        second = [18,19,20,21,26,29,34,37,42,43,44,45]
        third = [9,10,11,12,13,14,17,22,25,30,33,38,41,46,49,50,51,52,53,54]
        fourth = [0,1,2,3,4,5,6,7,8,15,16,23,24,31,32,39,40,47,48,55,56,57,58,59,60,61,62,63]
        cycles = [
            first,
            second,
            third,
            fourth,
        ]
        for cycle in cycles:
            for i in cycle:
                if str(i) not in self._balls.keys() and i not in self._balls.keys():
                    _ = self._set_pixel_color(i,scan_color)
                else:
                    print(f"Skipping Dragon Ball: {i}")
            _ = self._strip.show()
            time.sleep(0.4)
            for i in cycle:
                if str(i) not in self._balls.keys() and i not in self._balls.keys():
                    _ = self._set_pixel_color(i,self._default_color)
                else:
                    print(f"Skipping Dragon Ball: {i}")
            _ = self._strip.show()
            time.sleep(0.4)

    def ball_located(self):
        num = random.choice([27,28,29,35,36,37,43,44,45])
        if len(self._balls.keys()) == 7:
            return
        if str(num) in self._balls.keys() or num in self._balls.keys():
            return self.ball_located()
        self._set_pixel_color(num,self._orange,ball=True)
        return num

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

    def draw_circle_star(self, color=None):
        if not color:
            color = self._orange
        circle_star_pixels_1_indexed = [
            3, 4, 5, 6,
            10, 15,
            17, 24,
            25, 28, 29, 32,
            33, 36, 37, 40,
            41, 48,
            50, 55,
            59, 60, 61, 62
        ]
        # Convert 1-indexed to 0-indexed
        pixels = [i - 1 for i in circle_star_pixels_1_indexed]
        self._strip.fill((0, 0, 0))  # Clear display
        for i in pixels:
            self._strip[i] = color
        self._strip.show()

    def reset_balls(self):
        self._balls = {}
        self._pixel_colors = {n: self._default_color for n in range(self._numpix)}
        self._strip.fill(self._default_color)
        self._strip.show()
        if os.path.exists(self._ball_json):
            os.remove(self._ball_json)
        self._found_vendors_list = []
        if os.path.exists(self._found_vendors_json):
            os.remove(self._found_vendors_json)

    def get_mac_vendor(self, macaddr):
        macaddr = ":".join(macaddr.split(":")[0:3])
        mac_ven = self._mac_vendors.get(macaddr)
        if mac_ven:
            return mac_ven
        return

    def record_mac_vendor(self):
        if self._found_vendors_list:
            with open(self._found_vendors_json, 'w') as f:
                json.dump(self._found_vendors_list,f,indent=4)
        return

    def find_devices(self):
        mac_addrs = []
        async def scan_ble():
            devices = await BleakScanner.discover(timeout=2.0)
            return devices
        devices = asyncio.run(scan_ble())
        for device in devices:
            vendor = self.get_mac_vendor(device.address)
            if vendor:
                mac_addrs.append(vendor)
        return mac_addrs

    def run_sweep(self):
        print(f"Current Ball Locations: {list(self._balls.keys())}")
        devices_found = self.find_devices()
        print("Starting radar scan...")
        _ = self.run_radar_scan()
        print(f"Found {len(devices_found)} devices...")
        if devices_found:
            unique_devices_list = list(set(devices_found))
            for device in unique_devices_list:
                if device not in self._found_vendors_list:
                    print(f"New Device Found: {device}")
                    self._found_vendors_list.append(device)
                    pixel_num = self.ball_located()
                    print(f"Pixel Number Set: {pixel_num}")
            _ = self.record_mac_vendor()
            _ = self.blink_balls()
        print(f"Balls found: {len(list(self._balls.keys()))}")
        time.sleep(10)

def main():
    obj = BlueFinder()
    while True:
        if obj.done_check():
            obj.draw_circle_star()
            time.sleep(120)
            obj.reset_balls()
        else:
            obj.run_sweep()

if __name__ == '__main__':
    main()