from machine import Pin, PWM, Timer
from datetime import timedelta
import logging

class Drv8825:
  def __init__(self, dir: Pin, step: Pin, disable: Pin, acceleration_per_second = 2000, min_steps_per_second = 1500, max_steps_per_second = 1900):
    self._disable = disable
    self._dir = dir
    self._step = PWM(step)

    self._acceleration_interval = timedelta(milliseconds=10)
    self._acceleration_per_interval = int(acceleration_per_second / int(timedelta(seconds=1) / self._acceleration_interval))
    self._min_steps_per_second = min_steps_per_second
    self._max_steps_per_second = max_steps_per_second
    
    self._timeout_timer = Timer(-1)

    self._duty = int(65535 / 2)

    self.off()

  @classmethod
  def from_pin_ids(cls, dirId: str, stepId: str, disableId: str, acceleration_per_second = 2000, min_steps_per_second = 1500, max_steps_per_second = 1900):
    return Drv8825(
      dir=Pin(dirId, Pin.OUT),
      step=Pin(stepId, Pin.OUT),
      disable=Pin(disableId, Pin.OUT),
      acceleration_per_second=acceleration_per_second,
      min_steps_per_second=min_steps_per_second,
      max_steps_per_second=max_steps_per_second)

  def _accelerate(self, _):
    self._steps_per_second += self._acceleration_per_interval

    logging.debug("Accelerated to %s steps per second", self._steps_per_second)

    if self._steps_per_second > self._max_steps_per_second:
      self._steps_per_second = self._max_steps_per_second
      self._timeout_timer.deinit()

    self._step.freq(self._steps_per_second)

  def _start_motor(self):
    self._disable.off()
    
    self._steps_per_second = self._min_steps_per_second

    timeout_period = int(self._acceleration_interval / timedelta(milliseconds=1))
    self._timeout_timer.init(
      mode=Timer.PERIODIC,
      period=timeout_period,
      callback=self._accelerate)

    self._step.init(freq = self._steps_per_second, duty_u16 = self._duty)

  def off(self):
    self._disable.on()
    self._timeout_timer.deinit()
    self._step.deinit()

  def cw(self):
    self._dir.off()
    self._start_motor()
  
  def ccw(self):
    self._dir.on()
    self._start_motor()
