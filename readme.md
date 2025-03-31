# 🐉 Dragon Ball Radar (Raspberry Pi Edition)

Ever wish you could track down Dragon Balls like Bulma or Goku? This is a fun, geeky little program that runs on a **Raspberry Pi** and mimics the **Dragon Ball Radar** from Dragon Ball Z — using Bluetooth signals instead of mystical energy.

When it detects a high number of **unique Bluetooth MAC manufactures** nearby (like in a busy area), it displays a number of Dragon Balls (1–7) on an **LED matrix**, just like the classic radar.

## 💡 Concept

- Scan for **nearby Bluetooth devices**
- Count the number of **unique MAC manufactures**
- display between **1 and 7 Dragon Balls** on an **LED matrix**
- once 7 unique MAC manufactures are found, a large dragon call appears, and then it resets

## 🧰 What You’ll Need

- Raspberry Pi (any model with Bluetooth should work)
- LED Matrix Display 8x8
- Python 3
- Bluetooth support (Pi Zero or better)

## 📦 Installation
```
sudo apt-get -y install libbluetooth-dev python3-dev libboost-python-dev libboost-thread-dev libglib2.0-dev libgpiod2 python3-pip git
sudo nano /etc/dphys-swapfile
# change to 900
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
sudo free -m
git clone https://github.com/ltdenard/badge.git
cd badge
python3 -m venv env
soruce env/bin/activate
pip install -r requirements.txt
sudo cp -f badge.service /lib/systemd/system/
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable badge.service
sudo /bin/systemctl start badge.service
```
