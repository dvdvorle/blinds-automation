import network, rp2
import time

class Wifi:
   def __init__(self, country):
      self.country = country
   
   def connect(self, ssid, password):
      rp2.country(self.country)

      wlan = network.WLAN(network.STA_IF)
      # wlan.config(pm = 0xa11140) # Disable low power

      wlan.active(True)
      wlan.connect(ssid, password)

      # Wait for connect or fail
      max_wait = 20
      while max_wait > 0:
         if wlan.status() < 0 or wlan.status() >= 3:
            break
         max_wait -= 1
         print("connecting to", ssid)
         time.sleep(1)
         
   # Handle connection error
      if wlan.status() != 3:
         raise RuntimeError("connection failed with", wlan.status())
      else:
         print("connected to", ssid)
         status = wlan.ifconfig()
         self.ip = status[0]

         print("ip", self.ip)
