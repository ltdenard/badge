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
