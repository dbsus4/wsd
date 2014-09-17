#!/usr/bin/python

# wsd project main script

# hardware: ws2801 led strips + raspberry pi + internet adapter
# software pulls twits from an 'admin' (twits and retwits) and 
# displays the last result through the led strip 

# Written by Pratipo.org, hightly based on Adafruit's IoT Pinter. MIT license.
# MUST BE RUN AS ROOT (due to GPIO access)

import subprocess, time, socket, re
#from Wsd2 import *
from Twitter import *

prevTime = 0.0
interval = 10.0

tw = Twitter()
# display = Wsd2()

# time.sleep(20)
# display.setText('#wsd by idensitat+pratipo')
# display.rollPixels(True)

while(True):
	print "querying twitter"
	body = tw.getNewest()
	print body	
	# display.setText(body)
	# display.rollPixels(True)
	time.sleep(1)

