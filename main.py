#!/usr/bin/python

# wsd project main script

# hardware: ws2801 led strips + raspberry pi + internet adapter
# software pulls twits from an 'admin' (twits and retwits) and 
# displays the last result through the led strip 

# Written by Pratipo.org, hightly based on Adafruit's IoT Pinter. MIT license.
# MUST BE RUN AS ROOT (due to GPIO access)

import subprocess, time, socket, re
from Wsd2 import *
from Twitter import *

tw = Twitter()
display = Wsd2()

time.sleep(10)
display.setText('#wsd by idensitat+pratipo')
display.rollPixels(True)
time.sleep(0.01)

prev = ""


while(True):
	for x in range(0, 3):
		print "querying twitter"
		body = tw.getNewest()

		if (body != prev):
			print('fresh twit' + body)	
			#write new twit to file
			file = open('frases.txt', 'a')
			file.write(body+'\n')
			file.close()
			prev = body
	
		else:
			file = open('frases.txt', 'r')
			lines = file.read().splitlines()
			body =random.choice(lines)
			file.close()
		
			print('random twit' + body)	


		display.setText(body)
		display.rollPixels(True)
		time.sleep(0.01)

	display.setText('#TerritoriGuiri')
	display.staticPixels()
	time.sleep(0.01)

