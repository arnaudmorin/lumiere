#!/usr/bin/env python3
#
# Manage light through MQTT
#
# Author: Arnaud Morin <arnaud.morin@gmail.com>
# License: Apache 2

import paho.mqtt.client as mqtt
import json
import logging


class LumiereMqttClient(object):
    def __init__(self):
        # Init the logger
        self.logger = logging.getLogger('lumiere')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug('Starting logger')

        # Init the MQTT client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set('tasmota', 'tasmota')    # Yes, this is the password
        self.logger.debug('Connecting to Mosquitto')
        self.client.connect("127.0.0.1", 1883, 60)

    def on_connect(self, client, userdata, flags, rc):
        '''
        The callback for when the client receives a CONNACK response from the server.
        '''
        self.logger.debug('Connected to Mosquitto')

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("+/+/+")
        self.logger.debug('Subscribing to RESULT')
        client.subscribe("tele/bridge/RESULT")

    def on_message(self, client, userdata, msg):
        '''
        The callback for when a PUBLISH message is received from the server.
        '''
        try:
            if msg.topic == 'tele/bridge/RESULT':
                message = json.loads(msg.payload)

                if message['RfReceived']['Data'] == 'B8E488':
                    self.logger.info('Received B8E488 --> Alex ON')
                    client.publish('cmnd/lumiere/POWER', 'ON')

                elif message['RfReceived']['Data'] == 'B8E484':
                    self.logger.info('Received B8E484 --> Alex OFF')
                    client.publish('cmnd/lumiere/POWER', 'OFF')

                elif message['RfReceived']['Data'] == 'D8A0A8':
                    self.logger.info('Received D8A0A8 --> Arnaud ON')
                    client.publish('cmnd/lumiere/POWER', 'ON')

                elif message['RfReceived']['Data'] == 'D8A0A4':
                    self.logger.info('Received D8A0A4 --> Arnaud OFF')
                    client.publish('cmnd/lumiere/POWER', 'OFF')

                # Unknow code
                elif message['RfReceived']['Data']:
                    self.logger.info('Received {}'.format(message['RfReceived']['Data']))

        except Exception as e:
            self.logger.error('Error occured: {}'.format(e))

    def serve(self):
        '''
        Blocking call that processes network traffic, dispatches callbacks and
        handles reconnecting.
        Other loop*() functions are available that give a threaded interface and a
        manual interface.
        '''
        self.logger.info('Starting to serve')
        self.client.loop_forever()


if __name__ == '__main__':
    lumiere = LumiereMqttClient()
    lumiere.serve()
