#mqtt connection handler

import paho.mqtt.client as mqtt


def create_connection_handler(host, topic_prefix):
    if host:
        handler = host_con_handler(topic_prefix)
    else:
        handler = client_con_handler(topic_prefix)
    return handler

class host_con_handler():
    
    def __init__(self, topic_prefix):
        self.topic_prefix = topic_prefix
    
    def on_message(client, userdata, msg):
        pass
    def on_connect(client, userdata, flags, rc):
        pass

class client_con_handler():
    
    def __init__(self, topic_prefix):
        self.topic_prefix = topic_prefix
    
    def on_message(client, userdata, msg):
        pass
    def on_connect(client, userdata, flags, rc):
        pass

def mqtt_init(self):
    
    global client
    
    #mqtt innit
    client = mqtt.Client()
    client.on_message = self.on_message
    client.on_connect = self.on_connect
    
    client.username_pw_set("minesweeper", "pyarcade")
    
    #connect
    client.connect("pulspy.info", 1883, 60)
    client.loop_start()