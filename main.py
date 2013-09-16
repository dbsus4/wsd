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

#import RPi.GPIO as GPIO
import subprocess, time, Image, socket

nextInterval = 0.0
lastId = '1'   # State information passed to/from interval script


# Called at periodic intervals (30 seconds by default).
# Invokes twitter script.
def interval():
  p = subprocess.Popen(["python", "twitter.py", str(lastId)],stdout=subprocess.PIPE)
  r = p.communicate()[0] # Script pipes back lastId, returned to main
  print r
  return r

# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
 # GPIO.setmode(GPIO.BCM)

# Processor load is heavy at startup; wait a moment to avoid stalling during greeting.
#time.sleep(60)

# Main loop
while(True):
  t = time.time()

  # Every 30 seconds, run Twitter scripts.  'lastId' is passed around
  # to preserve state between invocations.  Probably simpler to do an
  # import thing.
  if t > nextInterval:
    print "next twitter query"
    nextInterval = t + 15.0
    
    #subprocess.call(["python", "test.py"])

    result = interval()
    if result is not None:
      lastId = result.rstrip('\r\n')

