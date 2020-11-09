#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from vcgencmd import Vcgencmd
Vc = Vcgencmd();
import sys,struct,smbus,sys,time,subprocess,threading
global Capacity, Volt, Temp, USV

###   Script settings   ###
minC=75       # min. Capacity from Battery in percent
mAh=540       # Li-Ion Capacity: example with 3Ah. Need for Current Calculation
ShutDown = "PowerOff"   # Set Command for Shutdown & Power Off
LogFile="/var/log/X708.log"

def Write(text):
   f = open(LogFile, "a+")
   f.write(text + '\n'); f.close();
   print (text);

# Read i2c from Geekworm X708 UPS
def X708(bit):
   bus = smbus.SMBus(1)   # 0 = i2c-0 || 1 = i2c-1
   read = bus.read_word_data(0x36, bit)   #i2c address=0x36
   swapped = struct.unpack("<H", struct.pack(">H", read))[0]
   if ( bit == 2 ):         # Read Voltage from bit: 2
        Volt = "%1.2f" % (swapped * 1.25 /1000/16); return str(Volt);
   elif ( bit == 4 ):      # Read Capacity from bit: 4
        Capacity = "%3.1f" % (swapped/256); return str(Capacity);

def PowerOff():   # switch bcm 13 on and poweroff for Shutdown
   Write('\n\n' + now + ' |--->>  Protection: UPS minimum Capcity reached: ' + str(X708(4)) + ' %   <<<---')
   # Calculate Current Consumption
   runtime = (int(time.time()) - t1)
   Icalc = ( Icalc * (100 - int(minC)) )
   Icalc = "%4.0f" % ( (Icalc * 60) / int(runtime) )
   Write(now + ' |-> Calculated Current: ' + str(Icalc) + 'mAh \n' + now + ' |-> USV runtime: ' + str(runtime) + ' s \n')
   time.sleep(5)
   process = subprocess.Popen(ShutDown.split(), stdout=subprocess.PIPE)
   output, error = process.communicate();

###  START   ###
now = time.strftime("%H:%M", time.localtime());
Write('\n\n' + now + ' |--->>>   Protection.py loaded   <<<---|\n' + now+' |-> PowerOFF Capacity: '+str(minC)+'%')
Write(now + ' |-> Battery Voltage: ' + X708(2) + ' V\n' + now + ' |-> Battery Capacity: ' + X708(4) + ' %')
LastCapacity = Capacity = X708(4)
t1=1

while True:
    now = time.strftime("%H:%M", time.localtime());
    Capacity = X708(4)
    if float(Capacity) > (float(LastCapacity) + 0.2):
        if ( int(t1) > 1 ):
            Write(now + ' |-> Protection: AC ON, Charging: ' + Capacity + '%')
            t1=1
        LastCapacity = Capacity
        time.sleep( (float(Capacity) * 5) / 3 )
    elif float(Capacity) < (float(LastCapacity) - 0.2):
        if ( int(t1) == 1 ):
             Icalc = ( mAh * (Capacity/100) )
             Write(now + ' |-> Protection: AC Lost, Capacity: ' + str(Capacity) + '%')
             t1 = (int(time.time()) - 60);  # add 60 s for better Calculation Icalc
        else:
             Status = now + ' |-> Status: '+X708(2)+'V - '+ X708(4)+'%'
             Status += ' | Time: '+str(int(time.time()) - t1) +'s'
             Show = Status;
             if ( float(Capacity) < (float(LastCapacity) - 1.5) ):
                  LastCapacity = Capacity
                  Write(Show)
             if float(Capacity) < float(minC):   # if USV Voltage to lower than minCapacity
                  PowerOff();
        time.sleep(float(Capacity))
    else:
        time.sleep( (float(Capacity) * 3) / 2)
