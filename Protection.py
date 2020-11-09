#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from vcgencmd import Vcgencmd
Vc = Vcgencmd();
import sys,struct,smbus,sys,time,subprocess,threading
global Capacity, Volt, Temp, USV

###   Script settings   ###
minC=70           # min. Capacity from Battery in percent
AC0=6         # Pin for AC Power Controll:  AC0 = 1 ==  AC LOST
AC_Timer=30       # Read and Log every seconds
Ah=0.5          # Li-Ion Capacity: example with 3Ah. Need for Current Calculation
LogFile="/var/log/X708.log"

# Use BCM-Map-> AC check: BCM-6 | Case Fan: BCM-26
GPIO.setwarnings(False); GPIO.setmode(GPIO.BCM);
GPIO.setup(AC0, GPIO.IN);

# Defaults
now = time.strftime("%H:%M", time.localtime());
Temp = str(Vc.measure_temp());
USV = GPIO.input(6)   # USV powered: 1  || AC powered: 0 ONLY in X708 Jumper Mode:0 

def Write(text):
   f = open(LogFile, "a+")
   f.write(text + '\n'); f.close();
#   print (text);

# Read i2c from Geekworm X708 UPS
def X708(bit):
   bus = smbus.SMBus(1)   # 0 = i2c-0 || 1 = i2c-1
   read = bus.read_word_data(0x36, bit)   #i2c address=0x36
   swapped = struct.unpack("<H", struct.pack(">H", read))[0]
   if ( bit == 2 ):         # Read Voltage from bit: 2
      Volt = "%1.2f" % (swapped * 1.25 /1000/16); return str(Volt);
   elif ( bit == 4 ):      # Read Capacity from bit: 4
      Capacity = "%i" % (swapped/256); return str(Capacity);

def PowerOff():   # switch bcm 13 on and poweroff for Shutdown
   Write('\n\n' + now + ' |--->>  Protection: UPS minimum Capcity reached: ' + str(Capacity) + ' %   <<<---')
   # Try to Calculate Current Consumption
   runtime = (int(time.time()) - t1)
   Icalc = ( (Ah*60) / int(runtime) )
   Write(now + ' |-> Calculated Current: ' + str(Icalc) + 'Ah \n' + now + ' |-> USV runtime: ' + str(runtime) + 's \n')
   CMD='PowerOff';
   process = subprocess.Popen(CMD.split(), stdout=subprocess.PIPE)
   output, error = process.communicate();

###  START   ###
Write('\n\n' + now + ' |--->>>   Protection.py loaded   <<<---|\n' + now+' |-> PowerOFF Capacity: '+str(minC)+'% <-|')
Write(now + ' |-> Battery Voltage: ' + X708(2) + ' V\n' + now + ' |-< Battery Capacity: ' + X708(4) + ' %')
LastCapacity = X708(4)
Capacity = X708(4)
t1=0.1
while True:
#   if USV == 0:    ## Wait for Edge Detection only on X708 Jumper Mode 0
#      GPIO.wait_for_edge(6, GPIO.RISING);
   if int(X708(4)) > int(LastCapacity):
      if ( int(t1) > 0.1 ):
         Write(now + ' |-> Protection: AC ON, Charging: ' + LastCapacity + '%')
         t1=0.1
      LastCapacity = X708(4)
      time.sleep(600)
   else:
      if int(X708(4)) < int(LastCapacity):
#      Write(now + ' |->>  AC POWER LOWER 90%  <-|')
         if ( int(t1) == 0.1 ):
            Write(now + ' |--->>>   Protection: AC Lost, Capacity: ' + LastCapacity + '%')
            t1 = int(time.time());
#   while USV == 1:
#      AC_ON=GPIO.wait_for_edge(6, GPIO.FALLING, timeout=(AC_Timer*1000))
         Temp = str(Vc.measure_temp());
         Status = 'Accu: '+X708(2)+'V - '+X708(4)+'%'
         Status += ' | Time: '+str(int(time.time()) - t1) +'s'
         Status += ' | Temp: '+str(Temp)+'°C'
         Show = '|->  '+Status+'  <-|'
#      if AC_ON is None:         # if timeout
         if int(X708(4)) > int(minC):   # if USV Capacity Okay
            Write(Show)
         else:       # if USV Voltage to LOW
            PowerOff();
         time.sleep(120)
      else:
         time.sleep(240)
