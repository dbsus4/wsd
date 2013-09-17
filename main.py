#!/usr/bin/python

# wsd project main script

# hardware: ws2801 led strips + raspberry pi + internet adapter
# software pulls twits from an 'admin' (twits and retwits) and 
# displays the last result through the led strip 

# Written by Pratipo.org, hightly based on Adafruit's IoT Pinter. MIT license.
# MUST BE RUN AS ROOT (due to GPIO access)

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

# Main loop

#idle until processor load settles
time.sleep(60)

while(True):
  t = time.time()
  if (t - prevTime > interval):
    prevTime = t
   
    print "next twitter query"
    #subprocess.call(["python", "test.py"])

    twit = getTwit()
    if twit is not None:
      body = twit.rstrip('\r\n')
      body = body.replace('#','')
      #body = body.upper()
      display.setText(body)
      display.rollPixels()


