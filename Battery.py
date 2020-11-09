#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import struct, smbus, sys, time, os
bus = smbus.SMBus(1)
GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM); GPIO.setup(13, GPIO.OUT);

#Voltage
voltage = bus.read_word_data(0x36, 2)
voltage = struct.unpack("<H", struct.pack(">H", voltage))[0]
voltage = voltage * 1.25 /1000/16
#Capacity
capacity = bus.read_word_data(0x36, 4)
capacity = struct.unpack("<H", struct.pack(">H", capacity))[0]
capacity = int(capacity/256)
#Write Text
print( "- Voltage:  " + str(voltage) + " V")
print( "- Capacity: " + str(capacity) + " %")

