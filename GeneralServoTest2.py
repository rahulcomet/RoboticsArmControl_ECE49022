from time import sleep
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

PIN = 17
factory = PiGPIOFactory()

servo = AngularServo(PIN, min_pulse_width = 0.0005, max_pulse_width = 0.0025, pin_factory = factory)

#Using preset values (min/mid/max) to control servo movement
print("servo positiob: middle")
servo.mid()
sleep(2)

print("servo position: min")
servo.min()
sleep(2)

print("servo position: max")
servo.max()
sleep(2)

print("servo position: mid")
servo.mid()
sleep(2)

#Using specific angle values to control servo movement
sleep(3)
print("Move servo to angle (degrees): 0")
servo.angle = 0
sleep(2)

print("Move servo to angle (degrees): -60 (anticlockwise)")
servo.angle = -60
sleep(2)

print("Move servo to angle (degrees): 0")
servo.angle = 0
sleep(2)

print("Move servo to angle (degrees): +60 (clockwise)")
servo.angle = 60
sleep(2)

print("Move servo to angle (degrees): 0")
servo.angle = 0
sleep(2)

servo.value = None
