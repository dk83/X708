#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from vcgencmd import Vcgencmd
#Vc = Vcgencmd();
import sys,struct,smbus,sys,time,subprocess,threading
global Capacity, Volt, Temp, USV, t1, LastCapacity

###   Script settings   ###
minC=75       # min. Capacity from Battery in percent
mAh=560       # Li-Ion Capacity: example with 3Ah. Need for Current Calculation
ShutDown = "PowerOff"   # Set Command for Shutdown & Power Off
LogFile = "/var/log/Do/Protection.log"
###   Init variables   ###
tolerance=0.7         # Tolerance for detect AC_ON  || AC_OFF
t1=1   # =1: AC_ON  |  =2: Wait for AC Status  |  >2:  AC_OFF  (t1 is a timer for battery runtime or detect charging)

# Define Logging
def Write(text):
   now = time.strftime("%H:%M", time.localtime());
   f = open(LogFile, "a+")
   f.write(now + ' |-> ' + text + '\n'); f.close();
   print (now + ' |-> ' + text);

# Read i2c from Geekworm X708 UPS
def X708(bit):
   bus = smbus.SMBus(1)   # 0 = i2c-0 || 1 = i2c-1
   read = bus.read_word_data(0x36, bit)   #i2c address=0x36
   swapped = struct.unpack("<H", struct.pack(">H", read))[0]
   if ( bit == 2 ):         # Read Voltage from bit: 2
        Volt = "%1.2f" % (swapped * 1.25 /1000/16); return str(Volt);
   elif ( bit == 4 ):      # Read Capacity from bit: 4
        Capacity = "%3.1f" % (swapped/256); return str(Capacity);
# Init Capacity value
LastCapacity = Capacity = X708(4);
#
def CalcAmpere(T):
    Icalc = int( mAh - ((float(Capacity)*mAh) / 100) );
    Icalc = "%4.0f" % ( (Icalc*3600)/int(T) );
    Write('Calculated Current Consumption: ' + str(Icalc) + 'mAh'); Sleep(1);

# Shutdown Raspberry and Power Off
def ShutDown_Now():
#   global t1, Icalc, minC;
   Write('SHUTDOWN,because minimum Capcity: ' + str(X708(4)) + ' % reached')
   # Calculate Current Consumption
   runtime = (int(time.time())-t1);
   CalcAmpere(int(runtime));
   Write('USV runtime: ' + str(runtime) + ' s');
   Sleep(10);
   process = subprocess.Popen(ShutDown.split(), stdout=subprocess.PIPE);
   output, error = process.communicate();

def Sleep(T):
#    Write('Sleep: ' + str(int(T)) + 's');
    time.sleep( int(T) )

###   Re-Init Capacity Variables   ###
def Var():
    global Capacity, LastCapacity;
    LastCapacity = Capacity = X708(4);

def AC_ON():
    Var(); global t1;
    if ( int(t1) > 1 ):
        CalcAmpere(int(time.time())-t1); t1=1;
        Write('AC Power ON, Charging: ' + Capacity + '%');

def AC_OFF():
    Var(); global t1, mAh, Icalc, Capacity, LastCapacity;
    if ( int(t1) == 1 ):
        Write('AC Power Lost with Capacity: ' + str(Capacity) + '%');
        t1 = (int(time.time())-3);
    else:
        Status = 'Status: ' + X708(2) + 'V - ' + X708(4) + '%';
        Status += ' | Time: ' + str(int(time.time()) - t1 ) + 's';
        Write(Status); Var();
        if float(Capacity) < float(minC):
            ShutDown_Now();

def AC():
#    global Capacity, LastCapacity;
    if float(Capacity) > (float(LastCapacity) + float(tolerance)):   # AC ON
        AC_ON();
    elif float(Capacity) < (float(LastCapacity) - float(tolerance)): # AC OFF
        AC_OFF();

###############
###   RUN   ###
#
Write('Protection.py loaded <-|\n');
Write('Shutdown Capacity: ' + str(minC) + '  %');
Write('Battery Voltage: ' + X708(2) + ' V');
Write('Battery Capacity: ' + X708(4) + ' %');


while True:
    Capacity = X708(4); AC();                       # Check:  AC ON  ||  AC OFF
    if (int(t1) > 1):           # if AC Power OFF ...
        Sleep(float(Capacity)/12);
    elif (float(Capacity) > 94):  # or AC ON && Capacity > 94% ...
        Sleep(5);      # This Sleep is used for 'AC OFF - Start Time: t1'
    else:                      # OR ...
        Sleep(10);
