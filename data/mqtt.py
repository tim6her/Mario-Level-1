# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'

import queue
import json

import paho.mqtt.client as mqtt

ACCELERATOR = 'MO_Fahrpedalrohwert_01'
BREAK = 'ESP_Bremsdruck'
STEARING = 'LWI_Lenkradwinkel'
STEARING_SGN = 'LWI_VZ_Lenkradwinkel'

SIMULATE = False
PORT_CAR = 1883
PORT_SIMULATOR = 1884

PORT = PORT_SIMULATOR if SIMULATE else PORT_CAR

Q_LENGTH = 0
STEAR_QUEUE = queue.LifoQueue(Q_LENGTH)
SGN_QUEUE = queue.LifoQueue()
ACC_QUEUE = queue.LifoQueue(Q_LENGTH)
BRK_QUEUE = queue.LifoQueue(Q_LENGTH)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('/signal/' + STEARING)
    client.subscribe('/signal/' + STEARING_SGN)
    client.subscribe('/signal/' + ACCELERATOR)
    client.subscribe('/signal/' + BREAK)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic, str(msg.payload))
    print(json.loads(msg.payload)['value'])
    value = json.loads(msg.payload)['value']
    if msg.topic == '/signal/' + ACCELERATOR:
        ACC_QUEUE.put(value)
        print('ACC', ACC_QUEUE.qsize())
    if msg.topic == '/signal/' + BREAK:
        BRK_QUEUE.put(value)
        print('BREAK', BRK_QUEUE.qsize())
    if msg.topic == '/signal/' + STEARING:
        STEAR_QUEUE.put(value)
        print('STEAR', STEAR_QUEUE.qsize())
    if msg.topic == '/signal/' + STEARING_SGN:
        SGN_QUEUE.put(value)
        print('SGN', SGN_QUEUE.qsize())

def run_mqtt():
    # Create an MQTT client and attach our routines to it.
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("82.165.25.152", PORT, 60)

    # Process network traffic and dispatch callbacks. This will also handle
    # reconnecting. Check the documentation at
    # https://github.com/eclipse/paho.mqtt.python
    # for information on how to use other loop*() functions
    client.loop_start()

if __name__ == '__main__':
    run_mqtt()
