#!/bin/bash

sudo modprobe gs_usb

sudo ip link set can0 up type can bitrate 500000

sudo modprobe usbserial

cd /dev/

sudo chown hunter ttyUSB0
