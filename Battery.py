#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import struct, smbus, sys, time, os
bus = smbus.SMBus(1)
GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM); GPIO.setup(13, GPIO.OUT);
R="\r\r\r\t\t\t";
#Voltage
voltage = bus.read_word_data(0x36, 2)
voltage = struct.unpack("<H", struct.pack(">H", voltage))[0]
voltage = "%1.2f" % float(voltage * 1.25 /1000/16)
#Capacity
capacity = bus.read_word_data(0x36, 4)
capacity = struct.unpack("<H", struct.pack(">H", capacity))[0]
capacity = "%3.1f" % (capacity/256);
#Write Text
print( "- Li-Ion Voltage:\r\r\r\t\t\t" + str(voltage) + " V")
print( "- Li-Ion Capacity:\r\r\r\t\t\t" + str(capacity) + " %")

