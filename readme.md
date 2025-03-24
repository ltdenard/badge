# 🐉 Dragon Ball Radar (Raspberry Pi Edition)

Ever wish you could track down Dragon Balls like Bulma or Goku? This is a fun, geeky little program that runs on a **Raspberry Pi** and mimics the **Dragon Ball Radar** from Dragon Ball Z — using Bluetooth signals instead of mystical energy.

When it detects a high number of **unique Bluetooth MAC addresses** nearby (like in a busy area), it displays a **random number of Dragon Balls** (1–7) on an **LED matrix**, just like the classic radar.

## 💡 Concept

- Scan for **nearby Bluetooth devices**
- Count the number of **unique MAC addresses**
- If the number exceeds a threshold (e.g. crowded place = magical energy)
- Randomly display between **1 and 7 Dragon Balls** on an **LED matrix**
- Profit (or wish for infinite pizza)

## 🧰 What You’ll Need

- Raspberry Pi (any model with Bluetooth should work)
- LED Matrix Display 8x8
- Python 3
- Bluetooth support (`bluez`, `pybluez`, etc.)
- `Pillow` for image rendering (if you're using a matrix library that supports it)
- `adafruit-circuitpython-neopixel`

## 📦 Installation
```
sudo apt-get install libbluetooth-dev bluez bluez-hcidump python-dev libboost-python-dev libboost-thread-dev libglib2.0-dev

sudo nano /etc/dphys-swapfile
# change to 900
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
sudo free -m
pip install gattlib

sudo cp -f /home/pi/badge/badge.service /lib/systemd/system/
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable badge.service
sudo /bin/systemctl start badge.service
```
