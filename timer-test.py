from datetime import timedelta
from machine import Pin, Timer
from utime import sleep
import socket

class x:
  def _run_timed_out(self, timer):
      print("hey")

  def main(self):
    max_run_duration = timedelta(seconds=3)

    _timeout_timer = Timer(-1)
    timeout_period = int(max_run_duration / timedelta(milliseconds=1))
    _timeout_timer.init(
          mode=Timer.ONE_SHOT,
          period=timeout_period,
          callback=self._run_timed_out)

    host_address = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(host_address)
    sock.listen(1)
    print("listening on", host_address)
    client, client_address= sock.accept()

foo = x()
foo.main()