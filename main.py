from machine import Pin
from utime import sleep

from wifi import Wifi
from motor_stepper import Motor_stepper, Step_rev_counter
from drv8825chip import Drv8825
import socket

import logging

logging.basicConfig(level=logging.DEBUG)
led = Pin("LED", Pin.OUT)
led.on()

motor_control = Drv8825.from_pin_ids(
    dirId="GP5",
    stepId="GP6",
    disableId="GP4",
    acceleration_per_second=4000,
    min_steps_per_second=5000,
    max_steps_per_second=5000)

rev_counter = Step_rev_counter("GP7", gear_ratio= 16, micro_steps_per_step= 64)

motor = Motor_stepper(
    motor_control,
    rev_counter,
    20
)

motor.calibrate_to(0)

wlan = Wifi("NL")
wlan.connect("", "")

host_address = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(host_address)
sock.listen(1)
print("listening on", host_address)

html = """<!DOCTYPE html>
<html>
<head> <title>Pico WH</title> </head>
<body> <h1>Pico WH</h1>
<p>Current status: %s</p>
<p><a href="/motor/cw">Turn CW</a></p>
<p><a href="/motor/ccw">Turn CCW</a></p>
<p><a href="/motor/off">Turn OFF</a></p>
</body>
</html>
"""

motor_status = "off"

while True:
    try:
        client, client_address= sock.accept()
        logging.debug("client connected from %s", client_address)
        request = str(client.recv(1024))[0:50]
        logging.debug(request)

        turn_cw = request.find('/motor/cw')
        turn_ccw = request.find('/motor/ccw')
        turn_off = request.find('/motor/off')

        if turn_cw >0:
            motor.move_to(20)
            motor_status = "turning cw"
        
        if turn_ccw >0:
            motor.move_to(0)
            motor_status = "turning ccw"

        if turn_off >0:
            motor.stop()
            motor_status = "off"

        response = html % motor.direction()

        client.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        client.send(response)
        client.close()

    except OSError as e:
        client.close()
        sock.close()
        
        print('connection closed')

    except KeyboardInterrupt:
        client.close()
        sock.close()
        print('connection closed')
        break

motor.stop()
led.off()

print("Finished.")
