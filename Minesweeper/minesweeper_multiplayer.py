import paho.mqtt.client as mqtt
import tkinter as tk
import minesweeper_singleplayer as ms
import time
import random
import string

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
    
def connect():
    global topic_prefix
    
    if ishost:
        topic_prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        conroot.clipboard_clear()
        conroot.clipboard_append(topic_prefix)
    else:
        topic_prefix = topic_entry.get()
        if len(topic_prefix) != 6:
            return
        
    topic_prefix = "minesweeper545158" + topic_prefix
    
    if ishost:
        conroot.destroy()
        ms.multiplayer = True
        ms.ishost = True
        
        ms.start_window()
        ms.root.after(100, check_started_status)
        ms.root.mainloop()
                

def check_started_status():
    global init_data
    global connected
    
    if not ms.start:
        if not connected:
            connected = True
            mqtt_init()
            
        ms.root.after(100, check_started_status)
    else:
        #after game was started by host
        
        #disable all buttons
        for r in ms.squares:
            for c in r:
                c.button.config(state="disabled")
                
        #read init_data from grid creation 
        init_data = f"{ms.gridsize};"
        for b in ms.bombs:
            coords = f"{str(b[0])},{str(b[1])}"
            init_data += f"{coords};"
        init_data = init_data[:-1]
        print(init_data)
        
        #next step
        ms.root.after(100, check_message_status)
        
def check_message_status():
    pass
def start_connect_window():
    global ishost
    global conroot
    global topic_entry
     
    
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
        client.subscribe("minesweeper545158" + topic_prefix)
    else:
        client.publish("minesweeper545158" + topic_prefix, init_data)
    client.subscribe("minesweeper545158" + topic_prefix)
    
    
    print(f"Connected with result code {rc}")
    
def on_disconnect(client, userdata, rc):
    global connected
    
    connected = False
        
def on_message(client, userdata, msg):
    print("okays")
    message = msg.payload.decode("utf-8")
    
    if msg.topic == topic_prefix:
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
    client.disconnect()
    print("closed connection")