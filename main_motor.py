from utime import sleep

from motor_stepper import Motor_stepper, Step_rev_counter
from drv8825chip import Drv8825


import logging

logging.basicConfig(level=logging.DEBUG)

motor_control = Drv8825.from_pin_ids(
    dirId="GP5",
    stepId="GP6",
    disableId="GP4",
    acceleration_per_second=4000,
    min_steps_per_second=5000,
    max_steps_per_second=25000)

rev_counter = Step_rev_counter("GP7", gear_ratio= 16, micro_steps_per_step= 64)

motor = Motor_stepper(
    motor_control,
    rev_counter,
    20
)

motor.calibrate_to(20)

try:
  motor.move_to(0)
  sleep(40)
finally:
  motor.stop()