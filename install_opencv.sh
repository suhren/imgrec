#!/bin/sh

echo 'Installing OpenCV'

echo 'Installing dependencies'
sudo apt install libgtk-3-dev \
                 libcanberra-gtk3-dev \
                 libtiff-dev \
                 zlib1g-dev \
                 libjpeg-dev \
                 libpng-dev \
                 libavcodec-dev \
                 libavformat-dev \
                 libswscale-dev \
                 libv4l-dev
                 libxvidcore-dev \
                 libx264-dev

echo 'Moving files'
tar xfv opencv-4.1.0-armhf.tar.bz2
sudo mv opencv-4.1.0 /opt
sudo cp -u opencv.pc /usr/lib/arm-linux-gnueabihf/pkgconfig

echo 'Modifying .bashrc'
LINE='export LD_LIBRARY_PATH=/opt/opencv-4.1.0/lib:$LD_LIBRARY_PATH'
FILE='.bashrc'
grep -qF -- "$LINE" "$FILE" || echo "$LINE" >> "$FILE"

#source .bashrc
#sudo bash -c 'echo "/opt/opencv-4.1.0/lib" > /etc/ld.so.conf.d/opencv-4.1.0.conf'

sudo mkdir -p /usr/lib/python2.7/dist-packages
sudo ln -s /opt/opencv-4.1.0/lib/python2.7/dist-packages/cv2 /usr/lib/python2.7/dist-packages/cv2
sudo mkdir -p /usr/lib/python3.7/dist-packages
sudo ln -s /opt/opencv-4.1.0/lib/python3.7/dist-packages/cv2 /usr/lib/python3.7/dist-packages/cv2