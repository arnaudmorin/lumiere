#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("+/+/+")
    client.subscribe("tele/bridge/RESULT")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    try:
        if msg.topic == 'tele/bridge/RESULT':
            message = json.loads(msg.payload)

            # Alex allumer
            if message['RfReceived']['Data'] == 'B8E488':
                print('Alex allumer')
                client.publish('cmnd/lumiere/POWER', 'ON')

            # Alex eteindre
            elif message['RfReceived']['Data'] == 'B8E484':
                print('Alex eteindre')
                client.publish('cmnd/lumiere/POWER', 'OFF')

            # Arnaud allumer
            elif message['RfReceived']['Data'] == 'D8A0A8':
                print('Arnaud allumer')
                client.publish('cmnd/lumiere/POWER', 'ON')

            # Alex eteindre
            elif message['RfReceived']['Data'] == 'D8A0A4':
                print('Arnaud eteindre')
                client.publish('cmnd/lumiere/POWER', 'OFF')

            # Nouveau code
            elif message['RfReceived']['Data']:
                print('Nouveau code: {}'.format(message['RfReceived']['Data']))

    except Exception as e:
        print('Error occurend {}'.format(e))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set('tasmota', 'tasmota')
client.connect("127.0.0.1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
