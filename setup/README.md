# ML on Embedded Systems

# Raspberry Pi

## Install 
https://www.raspberrypi.org/downloads/

## Enable SSH
On Raspberry:
Preferences -> Raspberry PI Configuration -> Interfaces -> SSH

If not installed:
(https://linuxize.com/post/how-to-enable-ssh-on-ubuntu-18-04/)
```
sudo apt update
sudo apt install openssh-server
```

Check if ssh service is running:
```
sudo systemctl status ssh
```

Make sure SSH is allowed in firewall:
```
sudo ufw allow ssh
```

Find IP address with e.g. one of the commands:
```
ifconfig -a
ip addr show
hostname -I
```

On other computer:
```
ssh pi@<ip>
```

Select yes to add key fingerprint
Type in password (default is "raspberry")

## Run Script
python3 app.py

## Run Docker
sudo docker run --device /dev/video0:/dev/video0 -p 8888:5000 suhren/imgrec-arm

# Jetson Nano

## SD Card Image
Download image for the target hardware from
https://developer.nvidia.com/embedded/downloads

* `sudo apt-get install unzip`
* `unzip ~/Downloads/nv-jetson-nano-sd-card-image-r32.3.1.zip`

Insert SD card

Find SD card with either
* `ls -la /dev/sd*`
* `sudo fdisk -l`
* `df -h`
* `dmesg | tail | awk '$3 == "sd" {print}'`

If needed:
`sudo apt-get install gparted`
`sudo gparted`
Select SD card and delete and merge all partitions

Flash SD card:
`sudo dd if=~/Downloads/sd-blob-b01.img of=/dev/sd<x> status=progress bs=4M`

or

Etcher:
https://www.balena.io/etcher/

Note: There will be unallocated space on the SD card. This can be expanded during the inital setup on the hardware.

Finally:
`sudo eject /dev/sd<x>`

## On JETSON

`sudo apt-get install python3.7`
`sudo apt-get install python3-pip`

Sudo important:
`sudo pip3 install virtualenv`

Find installed python verisons:
`ls /usr/bin/ | grep python`

OpenCV preinstalled for python versions in
`/usr/lib/python<x>/dist-packages/cv2`

Create virtual environment:
`virtualenv -p /usr/bin/python<x> <env>`
`cp /usr/lib/python<x>/dist-packages/cv2 <env>/lib/python<x>/dist-packages/cv2`

Test opencv in the environment:
```
source <env>/bin/activate
python 
import cv2
print cv2.__version__
```



## Nvidia SDK manager
Creat an account and log in to download the sdk manager from
https://developer.nvidia.com/nvidia-sdk-manager

sudo apt install ~/Downloads/sdkmanager_1.0.1-5538_amd64.deb

Open Nvidia SDK Manager and log in with your account

Select Target Hardware

## Login
user: nano
pass: nano

## SSH
On Jetson:
Find IP address with e.g. one of the commands:
```
ifconfig -a
ip addr show
hostname -I
```

On other computer:
```
ssh nano@<ip>
```

Select yes to add key fingerprint
Type in password (default is "nano")