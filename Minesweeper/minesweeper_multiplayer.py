import paho.mqtt.client as mqtt
import tkinter as tk
import minesweeper_singleplayer as ms
import time

ishost = False

def mqtt_init ():
    global client
    #mqtt innit
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    #connect
    client.connect("test.mosquitto.org", 1883, 60)
    client.loop_start()

def start_connect_window():
    global ishost
    global conroot
    
    def connect():
        global sub_topic
        global msg_topublish
        
        strlen = len(topic_entry.get())
        if not strlen >= 8:
            print(topic_entry.get()[:4])
            sub_topic =  topic_entry.get()[:8]
            
        else:
            print(topic_entry.get()[:4])
            sub_topic = topic_entry.get()[:strlen]
        
        
        
        if ishost:
            conroot.destroy()
            ms.multiplayer = True
            ms.ishost = True
            
            ms.start_window()
            while not ms.start:
                time.sleep(.1)
            msg_topublish = f"{ms.gridsize};"
            for b in ms.bombs:
                coords = f"{str(b[0])},{str(b[1])}"
                msg_topublish += f"{coords};"
            msg_topublish = msg_topublish[:-1]
            print(msg_topublish)    
            print(f"pubbed to {"minesweeperinit545158" + sub_topic}")
        
        mqtt_init()  
    
    def toggle_host():
        global ishost
        
        ishost = not ishost
        if ishost:
            host_toggle.config(text="Host")
        else:
            host_toggle.config(text="Client")
      
    conroot = tk.Tk()
    
    conroot.title("Verbinden")
    conroot.config(padx=15, pady=15)
    
    topic_text = tk.Label(conroot, text="Verbindungscode: ")
    topic_entry = tk.Entry(master=conroot)
    topic_button = tk.Button(master=conroot, text="Verbinden", command=connect, width=10)
    host_toggle = tk.Button(master=conroot, text="Client", command=toggle_host, width=6)
    
    for i in [topic_text,topic_entry, topic_button, host_toggle]:
        i.pack(side="left", padx = 10)
        
    conroot.mainloop()
    
def mqtt_disconnect ():
    client.disconnect()
    print("Verbindung getrennt")
    
def on_connect(client, userdata, flags, rc):
    global connected
    connected = True
    if not ishost:
        client.subscribe("minesweeperinit545158" + sub_topic)
    else:
        client.publish("minesweeperinit545158" + sub_topic, msg_topublish)
    client.subscribe("minesweepergame545158" + sub_topic)
    
    
    print(f"Connected with result code {rc}")
    
def on_disconnect(client, userdata, rc):
    global connected
    
    connected = False
        
def on_message(client, userdata, msg):
    print("okays")
    message = msg.payload.decode("utf-8")
    
    if msg.topic == "minesweeperinit545158" + sub_topic:
        print("war hier")
        ms.given_column_count = message.split(";")[0].split("x")[0]
        ms.given_row_count = message.split(";")[0].split("x")[1]
        bombs_raw = message.split(";")[1:]
        bombs = []
        for i in bombs_raw:
            bombs.append([int(i.split(",")[0]),int(i.split(",")[1])])
        ms.given_bombs = bombs
        conroot.destroy()
        ms.multiplayer = True
        ms.ishost = False
        
        ms.start_window()
        print(f"hallo {ms.bombs}")
            
    
    print(message)

if __name__ == "__main__":
    start_connect_window()