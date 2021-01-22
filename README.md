1) Install Raspberry Pi OS Lite
2) wpa_supplicant to /boot
3) ssh to /boot
4) Start computer
5) ssh into it
6) sudo raspi-config
- Timezone
- Localization
- Enable camera
7) sudo apt-get update & apt-get upgrade
8) sudo apt-get install sense-hat
9) sudo apt-get install python-pip
10) sudo pip install psutils
11) sudo nano /boot/config.txt
- Add a line at the end: dtoverlay: rpi-sense
12) sudo nano /etc/rc.local
- Add at the end but vefore exit 0: python /home/pi/sense/play.py # (or whatever is to be run)
