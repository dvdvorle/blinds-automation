# Prerequisites

## Install logging, typing, mqtt_as on microcontroller:
- Connect board to wifi
- run
  ``` py
  >>> import mip
  >>> mip.install("logging")
  >>> mip.install("github:peterhinch/micropython-mqtt")
  >>> mip.install("github:josverl/micropython-stubs/mip/typing_mpy.json")
  ```

## Configure the board
Upload a main_config.py file that looks like:

``` py
def settings():
  return (
    '<WIFI-name>',
    '<WIFI-pass>',
    '<mqtt-hostname>')

def source_settings():
    return (
    '<github-username>',
    '<github-project>',
    '<github-PAT>')
```

## Update command/topic
Change this line in app.py
``` py
command_topic = "woonkamer/gordijn"
```

# Running the software
Upload the rest of the project.

A first time calibration is needed. Using `mqttools` that could look like this:

`mqttools publish --host pi8.local woonkamer/gordijn "CALIBRATE 0"`