#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# Open SPI device
dev 		= "/dev/spidev0.0"
spidev 		= file(dev, "wb")
prevTime 	= 0.0
sel 		= True

L = 35*5

pixelA		= bytearray(L*3)
for h in range(L):
	i = h*3
	if h%2:
		pixelA[i+0] = int(255)
	else:
		pixelA[i+0] = int(0)

	pixelA[i+1] = int(0)
	pixelA[i+2] = int(0)

pixelB		= bytearray(L*3)
for h in range(L):
	i = h*3
	if not h%2:
		pixelB[i+0] = int(255)
	else:
		pixelB[i+0] = int(0)

	pixelB[i+1] = int(0)
	pixelB[i+2] = int(0)

def display():
	#print "displaying..."
	if(sel):
		#print pixelA
		spidev.write(pixelA)
	else:
		#print pixelB
		spidev.write(pixelB)

	spidev.flush()
	time.sleep(0.005)

# main
while(True):
	if (time.time() - prevTime > 1.0):
		prevTime = time.time()
		sel = not sel
		display()
