#!/usr/bin/python

# wsd project main script

# hardware: ws2801 led strips + raspberry pi + internet adapter
# software pulls twits from an 'admin' (twits and retwits) and 
# displays the last result through the led strip 

# Written by Pratipo.org, hightly based on Adafruit's IoT Pinter. MIT license.
# MUST BE RUN AS ROOT (due to GPIO access)

import RPi.GPIO as GPIO
import subprocess, time, socket
from Wsd2 import *

prevTime = 0.0
interval = 10.0
display = Wsd2()

# Called at periodic intervals (30 seconds by default).
# Invokes twitter script.
def getTwit():
  p = subprocess.Popen(["python", "twitter.py"],stdout=subprocess.PIPE)
  # script pipes back twit body
  twit = p.communicate()[0] 
  #print twit
  return twit

# Main loop

#idle until processor load settles
#time.sleep(30)

while(True):
  #t = time.time()
  #if (t - prevTime > interval):
    #prevTime = t
  display.setText('#dsntk4ever')
  display.rollPixels(True)

  print "next twitter query"
  twit = getTwit()
  print twit
  if (twit is None) or (twit is ''):
    display.setText('no connection')
    display.rollPixels(True)
  elif twit is not None:
    body = twit #.rstrip('\r\n')
    #if (len(body)>10):
      #body = body.replace('#','')
    body = body.upper()
    display.setText(body)
    display.rollPixels(True)


