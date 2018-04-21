#!/usr/bin/python

import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN)
 
for i in range(0,5):
    print GPIO.input(26)
