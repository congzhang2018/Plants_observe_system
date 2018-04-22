#!/usr/bin/python
import sys
import Adafruit_DHT
import time

humidity = 0
temperature = 0
while True:
    print "DH11 sensor start time: %.30f" %( time.time())
    for i in range(10):
        humidity1, temperature1 = Adafruit_DHT.read_retry(11, 4)
        humidity += humidity1
        temperature += temperature1
        print "DH11 counter:",i
    average_humidity = humidity/10
    average_temperature = temperature/10
    print "average_humidity %f, average_temperature %f" %(average_humidity, average_temperature)
    print "DH11 sensor end time: %.30f" %( time.time())
