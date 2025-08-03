from machine import Pin
from utime import sleep, ticks_ms
import math
from datetime import timedelta
from drv8825chip import Drv8825
from typing import Callable

from machine import PWM
import logging

class Step_rev_counter:
  def __init__(self, step: str, gear_ratio: int, micro_steps_per_step = 1, steps_per_rotation = 200):
    self._step = Pin(step, Pin.IN)
    self._shaft_revolution_count = steps_per_rotation * micro_steps_per_step
    self._output_revolution_count = self._shaft_revolution_count * gear_ratio
    self._steps = 0

    self._revolved_handler = lambda _ : None;
    self._stop_handler = lambda _ : None;

    self._step.irq(self.stepped, Pin.IRQ_RISING)

  def stepped(self, _):
    try:
      self._steps += 1

      if self._steps % self._output_revolution_count == 0:
        self._steps = 0
        self._revolved_handler()
    except KeyboardInterrupt:
      self._stop_handler()


  def notify(self, stepped_handler: Callable[[], None], stop_handler: Callable[[], None]):
    self._revolved_handler = stepped_handler
    self._stop_handler = stop_handler

class Motor_stepper:
  def __init__(self, motor_control: Drv8825, rev_counter: Step_rev_counter, rev_range: int):
    self._motor_control = motor_control
    self._rev_counter = rev_counter
    self.rev_range = rev_range
    self._position = 0
    self._direction = 0
    self.need_calibration = True

  def distance(self):
    return self.target_position - self._position
  
  def position(self):
    return self._position
  
  def direction(self):
    return self._direction

  def calibrate_to(self, target_position):
    if self._direction != 0:
      raise Exception("Can't calibrate while running")
    
    self._position = target_position
    self.need_calibration = False

  def move_to(self, target_position):
    self.target_position = target_position

    if not self._should_move():
      return
    
    self._direction = -1 if self.distance() < 1 else 1
    start_motor = self._motor_control.cw if self._direction < 1 else self._motor_control.ccw
    
    self._rev_counter.notify(self._revolved, self.stop)

    start_motor()

  def stop(self):
    if not self._running():
      return
    
    logging.debug("Stopping motor")

    self._direction = 0
    self._motor_control.off()

  def _should_move(self):
    return self.distance() != 0 and not self.need_calibration
  
  def _revolved(self):
    if not self._running():
        return
      
    self._position += self._direction
    logging.debug("Revolved, at %s, to %s", self._position, self.target_position)

    if not self._should_move():
      self.stop()

  def _running(self):
    return self._direction != 0