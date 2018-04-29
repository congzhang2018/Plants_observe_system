# Plants_observe_system

This project is a course project. It based on Raspberry Pi3 module B to build a Plants monitor system, it can observer the soil humidity level, environment temperature & humidity, and if it has light or not.

Because the output of soil humidity is an analog signal, and the Raspberry Pi does not support that, I have used Arduino to transfer the analog signal and send it by using serial communication to Raspberry Pi.

