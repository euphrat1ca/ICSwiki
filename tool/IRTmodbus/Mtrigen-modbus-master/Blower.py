#!/usr/bin/env python3
import RPi.GPIO as GPIO 
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

print("Initializing")
time.sleep(5)
PWM = GPIO.PWM(12,1000)
print("Running")
while 1==1:
	PWM.start(0)


