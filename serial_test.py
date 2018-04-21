#!/usr/bin/python

import serial
ser = serial.Serial('/dev/ttyACM0',9600)

while True:
		
		data = int(ser. readline())
		print  ('Data:' , data)
