#!/usr/bin/python

import RPi.GPIO as GPIO
import time

# Open SPI device
dev 		= "/dev/spidev0.0"
spidev 		= file(dev, "wb")
prevTime 	= 0.0
sel 			= True

pixelA		= [bytearray(3) for i in range(5)]
for i in range(len(pixelA)):
	if i%2:
		pixelA[i][0] = 255
		pixelA[i][1] = 0
		pixelA[i][2] = 0

pixelB		= [bytearray(3) for i in range(5)]
for i in range(len(pixelB)):
	if not (i%2):
		pixelB[i][0] = 255
		pixelB[i][1] = 0
		pixelB[i][2] = 0

def display():
	if(sel):
		print pixelA
		spidev.write(pixelA)
	else:
		print pixelB
		spidev.write(pixelB)

	spidev.flush()
	time.sleep(0.001)

# main
while(True):
	if (time.time() - prevTime > 1.0):
		prevTime = time.time()
		sel = not sel
		display()