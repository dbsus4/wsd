#!/usr/bin/python

# Main script for Adafruit Internet of Things Printer 2.  Monitors button
# for taps and holds, performs periodic actions (Twitter polling by default)
# and daily actions (Sudoku and weather by default).
# Written by Adafruit Industries.  MIT license.
#
# MUST BE RUN AS ROOT (due to GPIO access)
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

import RPi.GPIO as GPIO
import subprocess, time, socket
from Wsd import *

prevTime = 0.0
interval = 10.0
display = Wsd()

# Called at periodic intervals (30 seconds by default).
# Invokes twitter script.
def getTwit():
  p = subprocess.Popen(["python", "twitter.py"],stdout=subprocess.PIPE)
  # script pipes back twit body
  twit = p.communicate()[0] 
  print twit
  return twit

# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
 # GPIO.setmode(GPIO.BCM)

# Processor load is heavy at startup; wait a moment to avoid stalling during greeting.
#time.sleep(60)

# Main loop
while(True):
  t = time.time()
  if (t - prevTime > interval):
    prevTime = t
   
    print "next twitter query"
    #subprocess.call(["python", "test.py"])

    twit = getTwit()
    if twit is not None:
      body = twit.rstrip('\r\n')
      display.setText(body)
      display.rollPixels()


