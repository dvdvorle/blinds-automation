from machine import Pin
import logging

class Hbridge:
  def __init__(self, en12: Pin, in1: Pin, in2: Pin):
    self.en12 = en12
    self.en12.on()

    self.in1 = in1
    self.in2 = in2

  @classmethod
  def from_pin_ids(cls, en12Id: str, in1Id: str, in2Id: str):
    return Hbridge(
      en12=Pin(en12Id, Pin.OUT),
      in1=Pin(in1Id, Pin.OUT),
      in2=Pin(in2Id, Pin.OUT))

  def off(self):
      self.in1.off()
      self.in2.off()

  def on1(self):
      self.off()
      logging.debug("Turning on %s", self.in1)
      self.in1.on()

  def on2(self):
      self.off()
      logging.debug("Turning off %s", self.in2)
      self.in2.on()