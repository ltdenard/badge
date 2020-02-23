```
sudo cp -f /home/pi/badge/badge.service /lib/systemd/system/
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable badge.service
sudo /bin/systemctl start badge.service
```