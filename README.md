# RoboticsArmControl_ECE49022
Robotics Arm Control Subsystem for ECE 49022 Senior Design Project (Team 41: Arm.io).

This is a program designed to be run on the Raspberry Pi Compute Module 4. It's primary function is to read the linear instructions received via ethernet from the server subsystem and process them into servo motor instrucitons which it implements. 

## Libraries used (or might be used):

json

socket

sys

time

threading

multiprocessing

RPi.GPIO

adafruit_servokit

## Packages to be installed:

Adafruit_blinka:
pip3 install Adafruit-Blinka

Adafruit_CircuitPython_ServoKit:
sudo pip3 install adafruit-circuitpython-servokit


## Subsystem Block Diagram:

![BlockDiagramSubsystem drawio](https://user-images.githubusercontent.com/59933881/193178337-dd1214cc-b7f7-468e-979d-b1f820d30df3.png)

## Activity Diagram:

![Flow Diagram drawio](https://user-images.githubusercontent.com/59933881/193178313-dabad1da-87b2-4191-9aba-19034b65fe55.png)
