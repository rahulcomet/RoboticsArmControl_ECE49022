from time import sleep
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory

PIN = 17
factory = PiGPIOFactory()
servo = Servo(PIN, min_pulse_width = 0.0005, max_pulse_width = 0.0025, pin_factory = factory)

print("middle")
servo.mid()
sleep(5)
print("min")
servo.min()
sleep(5)
print("max")
servo.max()
sleep(5)
print("mid again")
servo.mid()
sleep(5)
servo.value = None