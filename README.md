# Plants_observe_system

This project is a course project. It based on Raspberry Pi3 module B to build a Plants monitor system, it can observer the soil humidity level, environment temperature & humidity, and if it has light or not.In the next, it will have three part: hardware, software, and the final results.

In the picture is this program's system. it shows the how this system work.

![Sys_diagram](https://github.com/congzhang2018/Plants_observe_system/blob/master/Picture/Sys_diagram.png)

## Hardware Part
  |Name|Picture|
  |:---|:---|
  |Soil humidity sensor|![Soil_sensor]（https://github.com/congzhang2018/Plants_observe_system/blob/master/Picture/soil_sensor.png ）
  |DH11 temperature & humidity sensor|![DH11]（https://github.com/congzhang2018/Plants_observe_system/blob/master/Picture/DH11.png ）
  |Photosensitive sensor|![Light_sensor]（https://github.com/congzhang2018/Plants_observe_system/blob/master/Picture/Light_sensor.png ）
  |Arduino UNO|![Arduino](https://store-cdn.arduino.cc/usa/catalog/product/cache/1/image/520x330/604a3538c15e081937dbfbd20aa60aad/a/0/a000066_featured_4.jpg)
  |Raspberry Pi 3 Model B|![Raspberry_pi](https://images-na.ssl-images-amazon.com/images/I/91zSu44%2B34L._SX355_.jpg)

## Software Part
* Raspberry Pi (Ubuntu Mate):  
  [Install MySQL](https://www.digitalocean.com/community/tutorials/how-to-install-the-latest-mysql-on-ubuntu-16-04#step-1-%E2%80%94-adding-the-mysql-software-repository)  
  [Install PHP and Apache server](https://howtoraspberrypi.com/how-to-install-web-server-raspberry-pi-lamp/)  
* Arduino UNO:
  Because Raspberry Pi can not read analog signal, I decide to using Arduino to read the Soil humidity sensor to read the analog signal and then using serial communication to send the data to Raspberry Pi. The code is in [soil_humidity_sensor_arduino](https://github.com/congzhang2018/Plants_observe_system/tree/master/soil_humidity_sensor_arduino) file.
* System Control Flow  
  ![Control_flow](https://github.com/congzhang2018/Plants_observe_system/blob/master/Picture/control_flow.png)  
  In this control flow, the program will get the data from sensors first, then it need to check if the data out of the request range to determine if it needs to send email. If it need send email, it will check if it sent email today, because we only want one remind email every day. Next, it need to save the data to database and record to a log file. At last, it will check if the day change, if it come to next day, the system need to reset some value, for example, the flag of send email, the flag of day. Meantime, it need close last time log file and open a new file for a new day.  
  In the program

## Final results
Now, this system can get the plants data and save it in the database, in the same time, it also can send the reminding message to the user to report the states of the plants. In the local network， any driver and visit the wed to see the real time data of the plants.
