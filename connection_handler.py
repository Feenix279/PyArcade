#mqtt connection handler

import paho.mqtt.client as mqtt
import tkinter as tk
import string
import random
import time
import threading

topic_prefix = "minesweeper3141"

try:
    creds = open("creds.crd", "r").read().split(";")
    broker = creds[0]
    user = creds[1]
    pw = creds[2]
except (FileNotFoundError, IndexError):
    import register_creds
    exit()
    
class host_con_handler():
    
    class client_class():
        def __init__(self, id:str):
            self.id:str = id
            self.timeout:int = time.time()+15
            self.is_timeouted = False
        
    def __init__(self):
        
        self.topic_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        print(self.topic_suffix)
        
        self.topic = topic_prefix + "/" + self.topic_suffix
        print(self.topic)
        
        self.init_data:str = None
        
        self.clients = []

        self.client:mqtt.Client = mqtt_init(self)
        

    def on_message(self, client, userdata, msg:mqtt.MQTTMessage):
        topic = msg.topic.replace(self.topic, "")
        message = msg.payload.decode('utf-8')
        print(message)
        print(topic)
        
        if topic== "/init":
            print(f"Sending init data to {message}")
            self.clients.append(self.client_class(message))
            id_list = []
            for i in self.clients:
                id_list.append(i.id)
            print(id_list)
            
            self.client.publish(f"{self.topic}/init/{message}", self.init_data)
                
    def publish_event(self):
        self.client.publish(f"{self.topic}/events")        
        

    def on_connect(self, client:mqtt.Client, userdata, flags, rc):
        self.client.subscribe(self.topic + "/init")
        if rc == 5:
            print("Nicht autorisiert, bitte korrekte Daten eintragen.")
            exit()
            
        print(f"connected with rc code {rc}")
        threading.Thread(target=self.timeout_handling, daemon=True).start()
        
        pass
    def reset_timeout(self, id):
        for i in self.clients:
            if i.id == id:
                i.timeout = time.time() + 15

    def timeout_handling(self):
        try:
            while True:
                time.sleep(10)
                self.client.publish(f"{self.topic}/timeout", "host")
                
                for i in self.clients:
                    if i.timeout < time.time():
                        i.is_timeouted == True
                        
                           
        except KeyboardInterrupt:
            pass

class client_con_handler():
    
    def __init__(self, topic_suffix:str):
        
        self.topic_suffix = topic_suffix
        self.topic = topic_prefix + "/" + self.topic_suffix
        
        self.id = str(round(time.time(),3))[-10:].replace(".","")
        print(f"Client Id: >{self.id}<")

        self.client:mqtt.Client = mqtt_init(self)
    
    def on_message(self, client, userdata, msg:mqtt.MQTTMessage):
        topic = msg.topic.replace(self.topic, "")
        message = msg.payload.decode("utf-8")
        if topic == f"/init/{self.id}":
            print("Received init data")
        if "moves" in topic and not self.id in topic:
            print("yay")
            
        elif msg.topic == "/events":
            print("received an event")
        
        print(f"Message received: >{message}<")
        
    
          
    def on_connect(self, client:mqtt.Client, userdata, flags, rc):
        print(f"connected with rc code {rc}")
        
        self.client.subscribe(f"{self.topic}/init/{self.id}")
        self.client.subscribe(f"{self.topic}/moves/#")
        
        self.client.subscribe(f"{self.topic}/events")

        #request init_data 
        self.client.publish(f"{self.topic}/init",self.id)
        print("sent init request")
        
    

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
    try:
        while True:

            selection = input("1. Host\n2. Client\n3. Trigger Event(Host)\nEingabe: ")

            try:
                selection = int(selection)
            except ValueError:
                print("Kein Integer")
            if selection == 1:
                handler = host_con_handler()
                handler.init_data = "Test init data"
            elif selection == 2:
                tp = input("Topic bidde: ")
                handler = client_con_handler(topic_suffix=tp)
            elif selection == 3:
                handler.client.publish("")

    except KeyboardInterrupt:
        handler.client.disconnect()
        exit()