from machine import Pin
from utime import sleep
from typing import Callable

class Hall_switch:
  def __init__(self, pinId : str):
    self.pin = Pin(pinId, Pin.OPEN_DRAIN, Pin.PULL_UP)

  def notify(self, handler: Callable[[], None]):
    self.pin.irq(lambda _ : handler(), Pin.IRQ_FALLING)