#!/usr/bin/python

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN)
#counter_light = 0
#counter_dark = 0
#for i in range(5):
#    print "light sensor start time:%.30f" %( time.time())
#    result = GPIO.input(26)
#   if result == 0:
#        counter_light += 1
#    else:
#        counter_dark += 1
#    current_light_time = counter_light * 2
#    current_dark_time = counter_dark * 2
#    print "counter_light:", counter_light
#    print "light sensor end time: %.30f" %( time.time())
while True:
    result = GPIO.input(26)
    time.sleep(0.5)
    print "result:", result
