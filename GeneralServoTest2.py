from time import sleep
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

PIN = 17
factory = PiGPIOFactory()

servo = AngularServo(PIN, min_pulse_width = 0.0005, max_pulse_width = 0.0025, pin_factory = factory)

#Using preset values (min/mid/max) to manipulate servo movement
print("middle")
servo.mid()
sleep(2)

print("min")
servo.min()
sleep(2)

print("max")
servo.max()
sleep(2)

print("mid again")
servo.mid()
sleep(2)

#Using specific angle values to manipulate servo movement
sleep(3)
print("0")
servo.angle = 0
sleep(2)

print("-60")
servo.angle = -60
sleep(2)

print("0")
servo.angle = 0
sleep(2)

print("+60")
servo.angle = 60
sleep(2)

print("0")
servo.angle = 0
sleep(2)

servo.value = None
