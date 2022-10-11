from time import sleep
import RPi.GPIO as GPIO
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
servo1 = AngularServo(17, min_pulse_width = 0.0005, max_pulse_width = 0.0025, pin_factory = factory)
servo2 = AngularServo(22, min_pulse_width = 0.0005, max_pulse_width = 0.0025, pin_factory = factory)
#servo3 = AngularServo(23, min_pulse_width = 0.0005, max_pulse_width = 0.0025, pin_factory = factory)

sleep(5)

#Using specific duty cycle values to control servo movement
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

p = GPIO.PWM(23, 50)
#initialize
p.start(2.5)

#extend arm: get in range of box
print("PWM Duty Cycle set at: 3.5%")
p.ChangeDutyCycle(3.5)
sleep(1)

#claw open/close using preset position values (min/mid/max) for servo control
print("claw status: open")
servo1.mid()
sleep(2)

#claw orientation using angle as parameters for servo control
print("Move servo to angle (degrees): 0")
servo2.angle = 0
sleep(2)

print("Move servo to angle (degrees): -60 (anti-clockwise)")
servo2.angle = -60
sleep(2)

print("Move servo to angle (degrees): 0")
servo2.angle = 0
sleep(2)

print("Move servo to angle (degrees): +60 (clockwise)")
servo2.angle = 60
sleep(2)

print("Move servo to angle (degrees): 0")
servo2.angle = 0
sleep(2)

servo2.value = None

#claw close: grab box
print("claw status: close")
servo1.max()
sleep(2)

#Extend arm up: pick up box
print("PWM Duty Cycle set at: 2.5%")
p.ChangeDutyCycle(2.5)
sleep(1)

#claw open: drop box
print("claw status: open again")
servo1.mid()
sleep(2)

servo1.value = None

p.stop()
GPIO.cleanup()