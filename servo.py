from machine import Pin
from utime import sleep, ticks_ms
import math
from datetime import timedelta

from machine import PWM

led = Pin("LED", Pin.OUT)
led.off()


motor = PWM(Pin("GP3"))

range_min = 500 * 1000
range_max = 2500 * 1000
range = range_max - range_min
neutral = range_min + range_max / 2

period = 2

motor = PWM(Pin("GP3"))
motor.freq(50)

try:

  while True:
    # Calculate normalized sine value between 0 and 1
    wave = (math.sin(ticks_ms() / 1000) + 1) / 2
    motor.duty_ns(int(wave * range + range_min))
    sleep(.1)

except KeyboardInterrupt:
  print("Finished")
  motor.deinit()