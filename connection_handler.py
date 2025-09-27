#mqtt connection handler

import paho.mqtt.client as mqtt
import tkinter as tk
import string
import random
import time
import threading

#todo: make prefix changeable in settings
topic_prefix = "minesweeper3141"
port = 1883

try:
    creds = open("creds.crd", "r").read().split(";")
    broker = creds[0]
    user = creds[1]
    pw = creds[2]
    if creds[3] != "":
        try:
            port = int(creds[3])
        except ValueError:
            pass

except (FileNotFoundError, IndexError):
    import register_creds
    exit()

#default func with high arg limit to prevent too many args on unassigned func --> bad workaround
def empty(one, two, three, four,five, six, seven, eigth, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen):
    pass
    
class host_con_handler():
    
    #object type for all clients connecting to host
    class client_class():
        def __init__(self, id:str):
            self.id:str = id
            self.timeout:int = time.time() + 15
            self.is_timeouted:bool = False
        
    def __init__(self, init=empty, move=empty, event=empty, timeouted=empty):
        
        #assigning funcs for events
        self.init = init
        self.move = move
        self.event = event
        self.timeouted = timeouted
        

        self.id = "host"
        #generate unique topic
        self.topic_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        print(self.topic_suffix)
        
        self.topic = topic_prefix + "/" + self.topic_suffix
        print(self.topic)
        
        #initiates the game and gets init data in return
        self.init_data:str = self.init()
        
        #creates clientlist to register and manage all future clients
        self.clients = []

        #starts mqtt
        self.client:mqtt.Client = mqtt_init(self)
        

    def on_message(self, client, userdata, msg:mqtt.MQTTMessage):
        
        #converts topic and message to usable formats
        topic = msg.topic.replace(self.topic, "")
        message = msg.payload.decode('utf-8')
        
        print(f"Topic: {topic}  Message: {message}")

        #disables all messages from host
        if message == "host" or "host" in topic:
                print("Eigene message, return")
                print("-------------------------------------")
                return        

        #specifies events for received messages
        
        #triggers timeout reset for specific client        
        if topic == "/timeout":            
            id = message
            self.reset_timeout(id)
            print(f"{id} meldet sich zum timeout check")
        
        #registers new client
        if topic == "/init":
            print(f"New Client registered")
            print(f"Sending init data to {message}")

            self.clients.append(self.client_class(message))
            self.client.publish(f"{self.topic}/init/{message}", self.init_data)

            #print client list
            id_list = []
            for i in self.clients:
                id_list.append(i.id)
            print(id_list)

        catch_general_topics(self, topic, message)
                
    def publish_event(self, message):
        self.client.publish(f"{self.topic}/events", message)
    
    def publish_move(self, move):
        self.client.publish(f"{self.topic}/moves/{self.id}", move)

    def on_connect(self, client:mqtt.Client, userdata, flags, rc):
        
        self.client.subscribe(self.topic + "/init")
        self.client.subscribe(self.topic + "/timeout")

        if rc == 5:
            print("Nicht autorisiert, bitte korrekte Daten eintragen.")
            exit()
            
        print(f"connected with rc code {rc}")

        threading.Thread(target=self.timeout_handling, daemon=True).start()        

    #resets timeout for client with given id
    def reset_timeout(self, id):
        
        for i in self.clients:
            if i.id == id:
                i.timeout = time.time() + 15
                print(f"Resetting timeout for client {i.id}")
                if i.is_timeouted == True:
                    i.is_timeouted == False
                    self.client.publish(f"{self.topic}/timeout/cleared", i.id)

    #background: sends timeout message and checks all clients 
    def timeout_handling(self):
        
        while True:
            time.sleep(10)
            self.client.publish(f"{self.topic}/timeout", "host")
            print("Checke Clients...")
            for i in self.clients:
                print(f"Checke Client {i.id}")
                if i.timeout < time.time():
                    if not i.is_timeouted:
                        i.is_timeouted = True
                        self.client.publish(f"{self.topic}/timeout/out", i.id)
                        print(f"{i.id} timed out")
                    
                    self.timeouted(i.id)

class client_con_handler():
    
    def __init__(self, topic_suffix:str="empty", init=empty, move=empty, event=empty, timeouted=empty):
        
        self.init = init
        self.move = move
        self.event = event
        self.timeouted = timeouted

        self.is_timeouted = True

        self.topic = topic_prefix + "/" + topic_suffix
        
        #generates random id 
        self.id = str(round(time.time(),3))[-10:].replace(".","")
        print(f"Client Id: >{self.id}<")

        #initiates mqtt 
        self.client:mqtt.Client = mqtt_init(self)
    
    def on_message(self, client, userdata, msg:mqtt.MQTTMessage):
        
        topic = msg.topic.replace(self.topic, "")
        message = msg.payload.decode("utf-8")

        print(f"Received: Topic: {topic};  Message: {message}")

        if topic == "/timeout":
            if message == "host":
                self.timeout = time.time() + 15
                if self.is_timeouted == True:
                    self.is_timeouted = False
                    self.timeouted("host", False)
                    print("Host reconnected")

        if topic == "/timeout/out":
            self.timeouted(message, True)

        if topic == "/timeout/cleared":
            self.timeouted(message, False)

        if topic == f"/init/{self.id}":
            threading.Thread(target=self.handle_timeout, daemon=True).start()
            print("Received init data")
        
        catch_general_topics(self, topic, message)
        
    
    def publish_move(self, move):
        self.client.publish(f"{self.topic}/moves/{self.id}", move)
    
          
    def on_connect(self, client:mqtt.Client, userdata, flags, rc):
        if rc == 5:
            print("Nicht autorisiert, bitte korrekte Daten eintragen.")
            exit()
        else:
            print(f"Connected with rc code {rc}")
        
        self.client.subscribe(f"{self.topic}/init/{self.id}")
        self.client.subscribe(f"{self.topic}/moves/#")

        self.client.subscribe(f"{self.topic}/timeout/cleared")
        self.client.subscribe(f"{self.topic}/timeout/out")
        self.client.subscribe(f"{self.topic}/timeout")
        
        
        self.client.subscribe(f"{self.topic}/events")

        #request init_data 
        self.client.publish(f"{self.topic}/init",self.id)
        print("sent init request")
    
    #background: publishes own timeout-stopper and checks for host every ten seconds
    def handle_timeout(self):
        while True:
            time.sleep(10)
            self.client.publish(f"{self.topic}/timeout", self.id)
            if self.timeout > time.time() and not self.is_timeouted:
                self.is_timeouted = True
                self.timeouted("host", True)
                print("Host timeouted")

def mqtt_init(handler:mqtt.Client):
    global client
    #mqtt innit
    client = mqtt.Client()
    client.on_message = handler.on_message
    client.on_connect = handler.on_connect
    client.on_disconnect = on_disconnect
    
    client.username_pw_set(user, pw)
    
    #connect
    client.connect(broker, port, 60)
    client.loop_start()

    return client

#fuses common topics for easier editing in the future
def catch_general_topics(self:(client_con_handler|host_con_handler), topic, message)->None:
    if "moves" in topic and not self.id in topic:
            print(f"Received move from {topic[-10:]}")
            self.move(message, topic[-10:])
            
    if topic == "/events":
        print("received an event")
        self.event(message, topic[-10:])

def on_disconnect(client, userdata, rc):
    print(f"Client disconnected with rc {rc}")

def default_ui(init=empty, move=empty, event=empty, timeouted=empty)->(client_con_handler|host_con_handler):
    import tkinter as tk
    def create_client_handler():
        handler =  client_con_handler(topic_entry.get(), init, move, event, timeouted)
        root.destroy()
        return handler
    def create_host_handler():
        handler = host_con_handler(init, move, event, timeouted)
        root.destroy()
        return handler
    
    root = tk.Tk()
    root.title("Multiplayer initialiser")

    handlers = tk.Frame(master=root)

    clientbutton = tk.Button(master=handlers, text="Client", command=create_client_handler)
    hostbutton = tk.Button(master=handlers, text="Host", command=create_host_handler)

    topic_entry = tk.Entry(master=root)
    exitbutton = tk.Button(master=root, text="Exit", command=exit)

    clientbutton.pack(padx=20, pady=5, side="right")
    hostbutton.pack(padx=20, pady=5, side="left")
    handlers.pack()
    topic_entry.pack()
    exitbutton.pack(padx=20, pady=5)
    
    root.mainloop()