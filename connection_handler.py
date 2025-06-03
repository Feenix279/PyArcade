#mqtt connection handler

import paho.mqtt.client as mqtt
import tkinter as tk
import string
import random

topic_prefix = "minesweeper3141"

creds = open("creds.crd", "r").read().split(";")
broker = creds[0]
user = creds[1]
pw = creds[2]

class host_con_handler():
    
    def __init__(self):
        self.topic_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        print(self.topic_suffix)
        self.topic = topic_prefix + "/" + self.topic_suffix
        print(self.topic)
        self.clients = []


        self.client = mqtt_init(self)
        

    def on_message(self, client, userdata, msg:mqtt.MQTTMessage):
        topic = msg.topic.replace(self.topic, "")
        message = msg.payload.decode('utf-8')
        print(message)
        print(topic)
        if topic.replace("/","") == "clreg":
            self.clients.append(message)
        

    def on_connect(self, client:mqtt.Client, userdata, flags, rc):
        self.client.subscribe(self.topic + "/clreg")
        print(f"connected with rc code {rc}")
        pass


class client_con_handler():
    
    def __init__(self, topic_suffix:str):
        self.topic_suffix = topic_suffix
        self.topic = topic_prefix + "/" + self.topic_suffix

        self.client = mqtt_init(self)
    
    def on_message(client, userdata, msg):
        msgpl = msg.payload.decode("utf-8")
        print(msgpl)
    def on_connect(self, client, userdata, flags, rc):
        print(f"connected with rc code {rc}")
        #self.client.publish()

def mqtt_init(handler:mqtt.Client):
    
    #mqtt innit
    client = mqtt.Client()
    client.on_message = handler.on_message
    client.on_connect = handler.on_connect
    client.on_disconnect = on_disconnect
    
    client.username_pw_set(user, pw)
    
    #connect
    client.connect(broker, 1883, 60)
    client.loop_start()

    return client
def on_disconnect(client, userdata, rc):
    print(f"Client disconnected with rc {rc}")
    
if __name__ == "__main__":
    global handler
    tp = "test"
    try:
        while True:

            selection = input("1. Host\n2. Client\nEingabe: ")

            try:
                selection = int(selection)
            except ValueError:
                print("Kein Integer")
            if selection == 1:
                handler = host_con_handler()
            elif selection == 2:
                handler = client_con_handler(topic_suffix=tp)

    except KeyboardInterrupt:
        handler.client.disconnect()
        exit()