#!/usr/bin/env python
# coding:utf-8

# Email lib
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import MySQLdb

# normal lib
import serial
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import logging
import sys
from datetime import datetime
from threading import Timer
from io import FileIO, BufferedWriter


LoggerWarningLevel = logging.DEBUG
# LoggerWarningLevel = logging.INFO
# LoggerWarningLevel = logging.WARNING
# LoggerWarningLevel = logging.ERROR

class Message:
    def __init__(self):
        subject = ''
        body = ''

class PlantMonitoring:

    def __init__(self):
        # initial GPIO port and serial communication
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26,GPIO.IN)
        self.ser = serial.Serial('/dev/ttyACM0',9600)
        soil_humidity1 = int(self.ser.readline())

        self.counter_dark = 0
        self.counter_light = 0

        # initial mysqldb

        # initial data and classes
        self.daily_report = Message()
        self.daily_report.subject = 'Plants state report!'
        self.warning_report = Message()
        self.warning_report.subject = 'Take care the plants!!'

        self.average_humidity = 10
        self.average_temperature = 10
        self.average_soil_humidity = 0
        self.current_light_time = 0
        self.current_dark_time = 0
        date = datetime.now()
        self.current_date = date.day

        self.send_warning_report = False
    """
    Send email
    """
    def SendEmail(self, message):

        fromaddr = "congzworking@gmail.com"
        toaddr = "zc188113236@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = message.subject

        body = message.body
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "zc188113236")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()

    """
    test the light
    """
    def GetLightingTime(self):

        result = GPIO.input(26)
        if result == 1:
            self.counter_light += 1
        else:
            self.counter_dark += 1

        self.current_light_time = self.counter_light * 5
        self.current_dark_time = self.counter_dark * 5


    """
    Recive soil mositure data form arduino
    """
    def GetSoilHumidity(self):
        soil_humidity = 0
        for i in range(10):
            soil_humidity1 = int(self.ser.readline())
            soil_humidity += soil_humidity1
            print "soil_humidity time:",i

        self.average_soil_humidity = (1-(soil_humidity/10.0/1024.0))*100
        print "soil_humidity precents:",self.average_soil_humidity
        

    """
    get humidity and temperature
    note: read-retry function read data every 2 seconds.
    """
    def GetTemperature(self):
        humidity = 0
        temperature = 0
        for i in range(10):
            humidity1, temperature1 = Adafruit_DHT.read_retry(11, 4)
            humidity += humidity1
            temperature += temperature1
            print "DH11:",i
        self.average_humidity = humidity/10
        self.average_temperature = temperature/10

    """
    Record data
    """
    def InitDataRecorder(self):
        self.counter_dark = 0
        self.counter_light = 0
        self.logger = logging.getLogger('Plants_monitoring_data')
        self.fileHandler_message = logging.StreamHandler(BufferedWriter(FileIO("Plants_monitoring_data" + time.strftime("%Y%m%d-%H%M%S") + ".log", "w")))
        self.logger.addHandler(self.fileHandler_message)
        self.formatter_message = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
        self.fileHandler_message.setFormatter(self.formatter_message)
        self.logger.setLevel(LoggerWarningLevel)
        self.logger.info('Time, soil_humidity, humidity, temperature, current_light_time, current_dark_time, total_light_time, total_dark_time')

    def RecordData(self):

        self.logger.info('%f,%f,%f,%f,%f,%f' %\
            (   time.time(),
                self.average_soil_humidity,
                self.average_humidity,
                self.average_temperature,
                self.current_light_time,
                self.current_dark_time,
            ))

        mysqldb = MySQLdb.connect(host="localhost",user="root",passwd="188113236",db="Plants",charset="utf8") 
        cursor = mysqldb.cursor()
        cursor.execute("show tables")
        cursor.execute("select * from table1")
        sql = 'insert into table1(id, temp, soil_humidity, humidity, light) values(720,%.2f, %.2f, %.2f, %.2f)'\
              % (self.average_temperature, self.average_soil_humidity, self.average_humidity, self.current_light_time)
        cursor.execute(sql)
        mysqldb.commit()
        cursor.execute("update table1 set id = id - 1")
        mysqldb.commit()
        mysqldb.close()

    def SigintHandle(self):
        self.logger.shutdown()
        self.logger.close()

    """
    Check if the plants need take care
    """

    def CheckLimition(self):
        print 'check limition!!!'
        date = datetime.now()
        if not self.send_warning_report:

            if self.average_soil_humidity < 63:

                self.warning_report.body = 'Your plants need Water!! Current state --> \n \
report data(mm/dd/yy): %d ,%d ,%d ,\n \
soil humidity: %f percents,\n \
temperature: %f Celsius,\n \
air humidity: %f percents,\n \
current lighting time: %f min' % \
(   date.month, date.day, date.year,
    self.average_soil_humidity,
    self.average_temperature,
    self.average_humidity,
    self.current_light_time
)

                self.SendEmail(self.warning_report)
                self.send_warning_report = True

            elif self.average_temperature < 5:
                self.warning_report.body = 'Your plants is cold!! Current state --> \n \
report data(mm/dd/yy): %d ,%d ,%d ,\n \
soil humidity: %f percents,\n \
temperature: %f Celsius,\n \
air humidity: %f percents,\n \
current lighting time: %f min' % \
(   date.month, date.day, date.year,
    self.average_soil_humidity,
    self.average_temperature,
    self.average_humidity,
    self.current_light_time
)
                self.SendEmail(self.warning_report)
                self.send_warning_report = True

            elif self.average_humidity > 65:
                self.warning_report.body = 'The surrounding humidity is too high, your plants need help!! Current state --> \n \
report data(mm/dd/yy): %d ,%d ,%d  ,\n \
soil humidity: %f percents,\n \
temperature: %f Celsius,\n \
air humidity: %f percents,\n \
current lighting time: %f min' % \
(   date.month, date.day, date.year,
    self.average_soil_humidity,
    self.average_temperature,
    self.average_humidity,
    self.current_light_time
)
                self.SendEmail(self.warning_report)
                self.send_warning_report = True


            else:
                return
        else:
            return

    def SendDailyReport(self):
        date = datetime.now()
        if self.current_lighting_time < 300:
            self.daily_report.body = 'The daily report for your plants!! You need make your plants have more light!! Current state --> \n \
report data(mm/dd/yy): %d ,%d ,%d ,\n \
soil humidity: %f percents,\n \
temperature: %f Celsius,\n \
air humidity: %f percents,\n \
current lighting time: %f min' % \
(   date.month, date.day, date.year,
    self.average_soil_humidity,
    self.average_temperature,
    self.average_humidity,
    self.current_light_time
)
            self.SendEmail(self.daily_report)
        else:
            self.daily_report.body = 'The daily report for your plants!! Current state --> \n \
report data(mm/dd/yy): %d ,%d ,%d  ,\n \
soil humidity: %f percents,\n \
temperature: %f Celsius,\n \
air humidity: %f percents,\n \
current lighting time: %f min' % \
(   date.month, date.day, date.year,
    self.average_soil_humidity,
    self.average_temperature,
    self.average_humidity,
    self.current_light_time
)
            self.SendEmail(self.daily_report)

plants = None
task = None

def initail():
    global plants

    plants = PlantMonitoring()
    plants.InitDataRecorder()

def Programming():
    print "Runing Programming"
    print "begin time", time.time()
    global task
    try:
        date = datetime.now()
        plants.GetTemperature()
        plants.GetLightingTime()
        plants.GetSoilHumidity()
        plants.CheckLimition()
        if plants.current_date == date.day:
            plants.RecordData()
        else:
            plants.SigintHandle()
            plants.InitDataRecorder()
            plants.RecordData()
            plants.SendDailyReport()
            plants.current_date = date.day
            plants.send_warning_report = False
        print "end time", time.time()
        task = Timer(120, Programming)
        task.start()
    except KeyboardInterrupt:
        print "End the program!"
        task.cancel()
        time.sleep(5)
        print '*******************************************************'
        print "The program has been ended!!"
        print '*******************************************************'

def main():
    try:
        initail()
        Programming()

    except KeyboardInterrupt:
        print "End the program!"
        task.cancel()
        time.sleep(5)
        print '*******************************************************'
        print "The program has been ended!!"
        print '*******************************************************'

if __name__ == "__main__":
    main()
