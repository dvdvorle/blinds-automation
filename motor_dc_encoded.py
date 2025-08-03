from datetime import timedelta
from machine import Pin, Timer
from hall_switch import Hall_switch
from hbridge import Hbridge
import logging

class Motor_dc_encoded:
  def __init__(self, motor_control: Hbridge, rev_counter: Hall_switch, rev_range: int, max_run_duration: timedelta):
    self._motor_control = motor_control
    self._rev_counter = rev_counter
    self.rev_range = rev_range
    self.max_run_duration = max_run_duration
    self._timeout_timer = Timer(-1)
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
    start_motor = self._motor_control.on1 if self._direction < 1 else self._motor_control.on2
    
    self._rev_counter.notify(self._revolved)

    timeout_period = int(self.max_run_duration / timedelta(milliseconds=1))
    logging.debug("Timeout periode is %s", timeout_period)
    self._timeout_timer.init(
      mode=Timer.ONE_SHOT,
      period=timeout_period,
      callback=self._run_timed_out)

    start_motor()

  def stop(self):
    if not self._running():
      return
    
    self._direction = 0
    self._motor_control.off()
    self._timeout_timer.deinit()

  def _should_move(self):
    return self.distance() != 0 and not self.need_calibration
  
  def _revolved(self):
    if not self._running():
        return
      
    self._position += self._direction
    logging.debug("Revolved, at %s, to %s", self._position, self.target_position)

    if not self._should_move():
      self.stop()
    
  def _run_timed_out(self, timer):
    if not self._running():
      return
    
    logging.debug("Motor timed out")
    print("Motor timed out")
    self.need_calibration = True
    self.stop()

  def _running(self):
    return self._direction != 0