from utime import sleep

from motor_stepper import Motor_stepper, Step_rev_counter
from drv8825chip import Drv8825
import logging

logging.basicConfig(level=logging.DEBUG)

motor_control = Drv8825.from_pin_ids(
    dirId="GP5",
    stepId="GP6",
    disableId="GP4",
    acceleration_per_second=500,
    min_steps_per_second=8000,
    max_steps_per_second=2000)

rev_counter = Step_rev_counter("GP7", gear_ratio= 16, micro_steps_per_step= 64)

motor = Motor_stepper(
    motor_control,
    rev_counter,
    25
)

motor.calibrate_to(3)

try:
  motor.move_to(0, 30000)
  while True:
    sleep(.5)
finally:
  motor.stop()