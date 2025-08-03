from motor_stepper import Motor_stepper, Step_rev_counter
from drv8825chip import Drv8825
default_speed = 4000
import logging
import ugit

motor_control = Drv8825.from_pin_ids(
  dirId="GP5",
  stepId="GP6",
  disableId="GP4",
  acceleration_per_second=4000,
  min_steps_per_second=4000,
  max_steps_per_second=default_speed)

rev_counter = Step_rev_counter("GP7", gear_ratio = 16, micro_steps_per_step = 64)

opened_revolutions = 28
motor = Motor_stepper(
  motor_control,
  rev_counter,
  opened_revolutions
)

motor.calibrate_to(0)
command_topic = "woonkamer/gordijn"
status_topic = command_topic + "/status"
should_notify_result = False

async def move_to(client, target_revolutions, status, speed : str | None = None):
  global should_notify_result
  motor.move_to(target_revolutions, int(speed or default_speed))
  await client.publish(status_topic, status, qos=1)
  should_notify_result = True

async def open(client, speed : str | None = None):
  await move_to(client, opened_revolutions, "opening", speed)

async def close(client, speed : str | None = None):
  await move_to(client, 0, "closing", speed)

async def calibrate(client, target : str):
  motor.calibrate_to(int(target))

async def update_source(client):
  logging.debug("Updating sources")
  ugit.pull_all()

actions = {
  "OPEN": open,
  "CLOSE": close,
  "CALIBRATE": calibrate,
  "UPDATE_SOURCE": update_source,
}

async def publish(client):
  global should_notify_result
  if should_notify_result and motor.direction() == 0:
    should_notify_result = False
    state = "closed" if motor.position() == 0 else "opened"
    logging.debug("Publishing {}".format(state))
    await client.publish(status_topic, state, qos = 1)