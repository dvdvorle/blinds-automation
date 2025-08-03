from mqtt_as import MQTTClient, config
import asyncio
import logging
import main_config
import ugit
import app

logging.basicConfig(level=logging.DEBUG)

(ssid, wifi_pw, server, github_user, github_repository, github_pat) = main_config.settings()
config['ssid'] = ssid
config['wifi_pw'] = wifi_pw
config['server'] = server

ugit.user = github_user
ugit.repository = github_repository
ugit.token = github_pat
ugit.ignore_files = ['/ugit.py', '/main_config.py']

async def up(client):  # Respond to connectivity being (re)established
  while True:
    await client.up.wait()  # Wait on an Event
    client.up.clear()
    
    await client.subscribe(app.command_topic, 1)  # renew subscriptions

async def messages(client):  # Respond to incoming messages
  global should_notify_result
  async for topic, msg, retained in client.queue:
    logging.debug("%s %s %s", topic.decode(), msg.decode(), retained)
    message_parts = msg.decode().split()
    if not message_parts:
      return

    command, *args = message_parts

    if command in app.actions:
      await app.actions[command](client, *args)

async def main(client):
  global should_notify_result
  await client.connect(quick=True)
  for coroutine in (up, messages):
    asyncio.create_task(coroutine(client))

  while True:
    await asyncio.sleep(5)
    await app.publish(client)

config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True
client = MQTTClient(config)
try:
  asyncio.run(main(client))
finally:
  client.close()  # Prevent LmacRxBlk:1 errors