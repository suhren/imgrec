# Cross compiling OpenCV 4
(https://solarianprogrammer.com/2018/12/18/cross-compile-opencv-raspberry-pi-raspbian/)

Usually, we compile exectuable code which is targeted for the same platform as the one we are compiling on. For example, if we compile code on a x86 platform, which is also targeted for an x86 platform.

This is however not always the case when we develop software for embedded systems, which often run on a completely different architecture, like arm32 or arm64. In these cases, we can't really just compile the code into binaries on our x86 machine and move them over to the arm32 machine. We need to make sure to *target* the compilation to the correct platform to make sure they are exectuable there.

An easy way of doing this is by simply compiling the binaries from the source code on the embedded system itself. E.g. by performing the compilation of the source code directly on a Raspberry Pi. This usually works out for small programs, and offers the advantage that we can quickly troubleshoot and debug any hardware-related issues, such as IO-access.

There are however a few *major* drawback with this approach when it comes to developing larger or more complex pieces of software. The first is the fact that we actually need access to the hardware itself to perform the compilation, which is not always possible. E.g. consider the case where we are working remotely or only have a limited number of hardware units to work on. The second is the relatively limited computation power of an embedded system like a Raspberry PI compared to a dedicated x86/amd64 workstation. Some larger software libraries which may take 10-15 minutes to compilte on a workstation might take hours (or even days!) to compile on an embedded system.

For these reasons, we can perform so called *cross compilation*. A cross compiler is capable of building the exectuable code for another platform than the one the compiler is running on itself.

## Cross compilation directly using the host OS

## Cross compilation using a Virtual Machine
It is a good idea to set up our cross comilation environment in a completely new and unused system. The reason for this is to make sure that the *armhf* libraries and exectuables we install won't conflict with the x86-64 versions in the host os.

### Installing KVM
In this example I will use KVM on Linux to create the virtual machine.
(https://www.howtogeek.com/117635/how-to-install-kvm-and-create-virtual-machines-on-ubuntu/)
(https://help.ubuntu.com/community/KVM/Installation)

KVM requires hardware virtualization support (AMD-V or Intel VT-x). We can see if our system has this by running
```
egrep -c '(svm|vmx)' /proc/cpuinfo
```

* 0 means that the CPU doesn't support hardware cirtualization
* 1 or greater means that the CPU does support hardware virtualization. We do however need to make sure it is also enabled in BIOS.

We can now install KVM with the following command
```
sudo apt-get install qemu-kvm libvirt-bin bridge-utils virt-manager
```

Only the root user and members of the `libvirtd` group can use KVM. We can therefore add our user to this group:
```
sudo adduser <username> libvirtd
```

(https://askubuntu.com/questions/930491/group-libvirtd-does-not-exist-while-installing-qemu-kvm)
There might be a problem with `Group 'libvirtd' does not exist while installing QEMU-KVM`. To fix this, we can run
```
sudo addgroup libvirtd
sudo adduser <username> libvirtd
```

We can now run the `virsh` command to see if the installation was successful:
```
virsh -c qemu:///system list
```

We can now start the Virtual Machine manager. Either open it through the applications in your desktio environment or run
```
virt-manager
```

(https://www.linux.com/audience/devops/creating-virtual-machines-kvm-part-1/)
By default images are stored in `/var/lib/libvirt`. This is part of the system root, and it is quite common with Linux systems that this is mounted on a separate, smaller partition of your drive (commonly limited to 10-24 GB). For this reason it is a good idea to create new directories in `/home/<username>/`

Create the followin two directories in your home folder (or anywhere you please):
* `/home/<username>/kvm-isos`
* `/home/<username>/kvm-pool`

We will use the latest release of Debian for the virtual machine. We can download an ISO image from https://www.debian.org/. Save this ISO to `/home/<username>/kvm-isos`.

### Creating the VM
We are now ready to create the virtual machine:
1. Go to `File -> New Virtual Machine`
1. Select local install media (ISO image or CDROM)
1. Select `Use ISO image` and `browse`
1. We are now presented with the Storage Volume Screen. On the left you can see the storage locations, and on the right you can see the contents of them.
    * Press the green `Add` button in the bottom left
    * Set the name to `kvm-pool` and the type to `dir: Filesystem Directory`
    * Go forward and set the target path to `/home/<username>/kvm-pool`
    * You should now see the new storage pool im the left pane.
    * Repeat this process again for `home/<username>/kvm-isos`
    * You should now see both the `kvm-pool` and `kvm-isos` in the left pane of the Storage Volume window.
1. Select your downloaded ISO from the `kvm-isos` storage and press `Choose Volume` and `Forward`.
1. You can now choose how much memory and how many CPUs will be allocated to the virtual machine. This is dependent on how much is available in your owns system of course, but I would suggest at least 2048 MB RAM and 1 CPU. 
1. Select `Enable storage for this virtual machine` and `Select or create custom storage` and `Manage...`
1. Select `kvm-pool` and create a new volume with the green plus sign in the top of the right panel.
1. Name the volume something like `debian-cross-compile.qcow2` and the format `qcow2`. Set the max capacity to 20.0 GiB (dependent on how much is needed by the cross compilation). Finally press `Finish`.
1. Now select your new storage volume and press `Choose Volume`.
1. Move forward and set the name of your new VM and press `Finish`.
1. Go through the installation steps of the OS on the VM.

The following steps are specifically for installing Debian on the VM:
(Note: to move the mouse cursour out from the VM window you can press CTRL + ALT)
1. Select Graphical install
1. Select language, location and keyboard layout
1. Create a user with a password
1. Select `Guided - use entire disk` -> Select the disk -> `All files in one partition`
1. Wait for the install to finish and configure the package manager with the default values.
    * (http://forums.debian.net/viewtopic.php?t=71051) When prompted if to install the GRUB bootloader to the master boot record, select yes and select the only drive.
1. The VM should now be set up!

### Sharing a folder between the host and VM
(https://nts.strzibny.name/how-to-set-up-shared-folders-in-virt-manager/)
It is now convinient to set up a shared folder which can be used to move files between the host system and the VM.
1. On the host, create a folder: `mkdir ~/vmshare`
1. Set up the permissions: `chmod 777 ~/vmshare`
1. In the virt-manager, got to `View > Details > Attach Hardware > Filesystem`
1. Set the following settings:
    * Type: Mount
    * Driver: Default
    * Mode: Mapped
    * Source path: `/home/<username>/vmshare`
    * Target path: `share` (this can be any name and will not be the name of the folder)
1. Make sure to shutdown and restart the VM.
1. In the VM, create the shared folder like `mkdir /vmshare`
1. Mount it with `sudo mount -t 9p -o trans=virtio share /vmshare`
1. You should now be able to share files using this folder.
1. If we want the folder to be available every time we restart the VM, we can add the following row to `/etc/fstab`: `share   /vmshare    9p  trans=virtio,version=9p2000.L,rw    0   0`
1. We also need to add the following rows to `etc/moduels/` to make sure the needed kernel modules are loaded at boot time. Otherwise we might get an error during boot (even though it may work when we press enter)
```
9p
9pnet
9pnet_virtio
```
1. Now, when the VM is restarted, we should still have access to the shared folder!


### Preparing the VM for cross-compilation
Make sure our VM is up to date:
```
sudo apt update
sudo apt upgrade
```

We can now enable the *armhf* architecture:
```
sudo dpkg --add-architecture armhf
sudo apt update
sudo apt install qemu-user-static
```

We will build OpenCV with support for Python and C++:
```
sudo apt-get install python3-dev
sudo apt-get install python3-numpy
sudo apt-get install python-dev
sudo apt-get install python-numpy
```

We also need *libpython* for the *armhf* architecture:
```
sudo apt-get install libpython2-dev:armhf
sudo apt-get install libpython3-dev:armhf
```

The following libraries are needed for GUI programs. If we are only going to run OpenCV without GUI we can ignore these.
```
sudo apt install libgtk-3-dev:armhf libcanberra-gtk3-dev:armhf
```

The following image and video format libraries are also required by OpenCV:
```
sudo apt install libtiff-dev:armhf zlib1g-dev:armhf
sudo apt install libjpeg-dev:armhf libpng-dev:armhf
sudo apt install libavcodec-dev:armhf libavformat-dev:armhf libswscale-dev:armhf libv4l-dev:armhf
sudo apt-get install libxvidcore-dev:armhf libx264-dev:armhf
```

We can now install the cross compilers to create *armhf* binaries for the Raspberry PI:
```
sudo apt install crossbuild-essential-armhf
sudo apt install gfortran-arm-linux-gnueabihf
```

Also install Cmake, git, pkg-config and wget:
```
sudo apt install cmake git pkg-config wget
```

Next, we can download the current release of OpenCV:
```
cd ~
mkdir opencv_all && cd opencv_all
wget -O opencv.tar.gz https://github.com/opencv/opencv/archive/4.1.0.tar.gz
tar xf opencv.tar.gz
wget -O opencv_contrib.tar.gz https://github.com/opencv/opencv_contrib/archive/4.1.0.tar.gz
tar xf opencv_contrib.tar.gz
rm *.tar.gz
```

We need to modify two system variables to build *GTK+* support:
```
export PKG_CONFIG_PATH=/usr/lib/arm-linux-gnueabihf/pkgconfig:/usr/share/pkgconfig
export PKG_CONFIG_LIBDIR=/usr/lib/arm-linux-gnueabihf/pkgconfig:/usr/share/pkgconfig
```

We can now use *Cmake* to generate the OpenCV build scripts:
```
cd opencv-4.1.0
mkdir build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/opt/opencv-4.1.0 \
      -D CMAKE_TOOLCHAIN_FILE=../platforms/linux/arm-gnueabi.toolchain.cmake \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_all/opencv_contrib-4.1.0/modules \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D ENABLE_NEON=ON \
      -D ENABLE_VFPV3=ON \
      -D BUILD_TESTS=OFF \
      -D BUILD_DOCS=OFF \
      -D PYTHON2_INCLUDE_PATH=/usr/include/python2.7 \
      -D PYTHON2_LIBRARIES=/usr/lib/arm-linux-gnueabihf/libpython2.7.so \
      -D PYTHON2_NUMPY_INCLUDE_DIRS=/usr/lib/python2/dist-packages/numpy/core/include \
      -D PYTHON3_INCLUDE_PATH=/usr/include/python3.7m \
      -D PYTHON3_LIBRARIES=/usr/lib/arm-linux-gnueabihf/libpython3.7m.so \
      -D PYTHON3_NUMPY_INCLUDE_DIRS=/usr/lib/python3/dist-packages/numpy/core/include \
      -D BUILD_OPENCV_PYTHON2=ON \
      -D BUILD_OPENCV_PYTHON3=ON \
      -D BUILD_EXAMPLES=OFF ..
```

If there were no errors, there should now be a *Makefile* in the *build* folder. We can now start the build which will take a relatively long time depending on your hardware (for me it took around 30 minutes with 2 allocated cores to the VM). The build is started with
```
make -j16
```

```
sudo make install/strip
```

```
cd /opt/opencv-4.1.0/lib/python3.7/dist-packages/cv2/python-3.7/
sudo cp cv2.cpython-37m-x86_64-linux-gnu.so cv2.so
```

```
cd /opt
tar -cjvf ~/opencv-4.1.0-armhf.tar.bz2 opencv-4.1.0
cd ~
```

`pkg-config` is the software which is responsible for installing software. It gives the installation scripts a common interface to query already installed libraries to compile any software which depends on them. 

We can define a package config file sor this purpose:

```
nano opencv.pc
```

```
libdir = /opt/opencv-4.1.0/lib
includedir = /opt/opencv-4.1.0/include/opencv4

Name: OpenCV
Description: OpenCV (Open Source Computer Vision Library) is an open source computer vision and machine learning software library.
Version: 4.1.0
Libs: -L${libdir} -lopencv_aruco -lopencv_bgsegm -lopencv_bioinspired -lopencv_calib3d -lopencv_ccalib -lopencv_core -lopencv_datasets -lopencv_dnn_objdetect -lopencv_dnn -lopencv_dpm -lopencv_face -lopencv_features2d -lopencv_flann -lopencv_freetype -lopencv_fuzzy -lopencv_gapi -lopencv_hfs -lopencv_highgui -lopencv_imgcodecs -lopencv_img_hash -lopencv_imgproc -lopencv_line_descriptor -lopencv_ml -lopencv_objdetect -lopencv_optflow -lopencv_phase_unwrapping -lopencv_photo -lopencv_plot -lopencv_quality -lopencv_reg -lopencv_rgbd -lopencv_saliency -lopencv_shape -lopencv_stereo -lopencv_stitching -lopencv_structured_light -lopencv_superres -lopencv_surface_matching -lopencv_text -lopencv_tracking -lopencv_videoio -lopencv_video -lopencv_videostab -lopencv_xfeatures2d -lopencv_ximgproc -lopencv_xobjdetect -lopencv_xphoto
Cflags: -I${includedir}
```

This tells the system that the libraries can be found in `/opt/opencv-4.1.0/lib` and its headers in `/opt/opencv-4.1.0/include/opencv4`. It also tells us that the name of the library is `OpenCV` and that the version is `4.1.0`. We also have a list of dependent libraries that need to be compiled by programs using this software. There is also a list of additional linker flags that must be used by code using this library.

```
sudo apt install libgtk-3-dev libcanberra-gtk3-dev
sudo apt install libtiff-dev zlib1g-dev
sudo apt install libjpeg-dev libpng-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
```


## Cross compilation using Docker
