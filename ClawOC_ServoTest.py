from time import sleep
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory

PIN = 17
factory = PiGPIOFactory()

servo = AngularServo(PIN, min_pulse_width = 0.0005, max_pulse_width = 0.0025, pin_factory = factory)

print("open")
servo.mid()
sleep(2)
print("close")
servo.max()
sleep(2)
print("open again")
servo.mid()
sleep(2)

servo.value = None