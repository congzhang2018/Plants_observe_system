#!/usr/bin/python

import serial
import time

ser = serial.Serial('/dev/ttyACM0',9600)
soil_humidity1 = 0
average_soil_humidity = 0
while True:
        print "soil sensor start time: %.30f" %( time.time())
        soil_humidity = 0
        for i in range(10):
            soil_humidity1 = int(ser.readline())
            soil_humidity += soil_humidity1
            print "soil_humidity counter:",i

        average_soil_humidity = (1.0-(((soil_humidity/10.0)-328.0)/695.0))*100
        print "soil_humidity precents:",average_soil_humidity
        print "soil sensor end time: %.30f" %( time.time())
#        soil_humidity1 = int(ser.readline())
#        print "soil_humidity", soil_humidity1
#        time.sleep(1)
