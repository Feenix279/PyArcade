import paho.mqtt.client as mqtt
import tkinter as tk
import minesweeper_singleplayer as ms
import time
import random
import string

ishost = False
connected = False
last_square = None
qos = 1
#general start code   
def connect():
    global topic_prefix
    
    if ishost:
        topic_prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        conroot.clipboard_clear()
        conroot.clipboard_append(topic_prefix)
        print(topic_prefix)
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
    #not host
    else:
        conroot.destroy()
        ms.multiplayer = True
        ms.ishost = False
        
        ms.start_window()
        ms.start_button.config(state="disabled")
        ms.size_input.config(state="disabled")
        ms.bomb_input.config(state="disabled")
        
        mqtt_init()
        
        ms.root.mainloop()
         
#host code
def check_started_status():
    global init_data
    global connected
    
    if not ms.start:
        if not connected:
            connected = True
            mqtt_init()
        ms.root.after(100, check_started_status)
    
    #after host started game
    else:
        print("Detected initialisation")
        #after game was started by host
        
        #disable all buttons
        for r in ms.squares:
            for c in r:
                c.button.config(state="disabled")
        
        ms.start_button.config(state="disabled")
        ms.size_input.config(state="disabled")
        ms.bomb_input.config(state="disabled")
                
        #read init_data from grid creation 
        init_data = f"{ms.gridsize};"
        for b in ms.bombs:
            coords = f"{str(b[0])},{str(b[1])}"
            init_data += f"{coords};"
        init_data = init_data[:-1]
        print(init_data)
        
        client.subscribe(topic=topic_prefix + "/announcement", qos=qos)
        print(f"Waiting for announcement with topic {topic_prefix + "/announcement"} ...")

#general code
def mqtt_init ():
    global client
    #mqtt innit
    client = mqtt.Client()
    client.username_pw_set("minesweeper", "pyarcade")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    #connect
    client.connect("pulspy.info", 1883, 60)
    client.loop_start()
    
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
        client.publish(topic=topic_prefix + "/announcement", payload = "Hello World", qos=qos)
        client.subscribe(topic = topic_prefix + "/init_data", qos=qos)
    
    print(f"Connected with result code {rc}")

#sweeper square saves itself in global variable once pressed
def check_moves():
    global last_square
    if ms.last_square_pressed != last_square:
        position = [ms.last_square_pressed.x, ms.last_square_pressed.y]
        position = str(position)
        if ishost:
            client.publish(topic=topic_prefix + "/hostmove", payload=position, qos=qos)
        else:
            client.publish(topic=topic_prefix + "/clientmove", payload=position, qos=qos)
        last_square = ms.last_square_pressed

    ms.root.after(50, check_moves)
def on_message(client, userdata, msg):
    
    message = msg.payload.decode("utf-8")
    print(f"Message received: {message}")
    #host subs
    if msg.topic == topic_prefix + "/announcement":
        print("Received announcement")
        client.publish(topic = f"{topic_prefix}/init_data", payload = init_data, qos=qos)
        for r in ms.squares:
            for c in r:
                if c.bombcount or c.isbomb:
                    c.button.config(state="normal")
                
        client.subscribe(topic=topic_prefix + "/clientmove", qos=qos)
        ms.root.after(100, check_moves)
        print(f"Feld erstellt, warte auf move von Client")
    
    #client subs
    if msg.topic == topic_prefix + "/init_data":
        print("Data was init data")
        
        ms.given_column_count = message.split(";")[0].split("x")[0]
        ms.given_row_count = message.split(";")[0].split("x")[1]
        
        bombs_raw = message.split(";")[1:]
        bombs = []
        
        for i in bombs_raw:
            bombs.append([int(i.split(",")[0]),int(i.split(",")[1])])
            
        ms.given_bombs = bombs
        ms.multiplayer = True
        ms.ishost = False
        
        ms.create_grid()
        ms.root.update()
        ms.root.after(100, check_moves)
        client.subscribe(topic_prefix+"/hostmove",qos=qos)
        
        print(f"Feld erstellt, warte auf move von Host")
    #general subs
    if msg.topic == topic_prefix + "/hostmove" and not ishost or msg.topic == topic_prefix + "/clientmove" and ishost:
        
        position = message.replace("[","").replace("]","").replace(" ","").split(",")
        print(f"Received move from {msg.topic.replace(topic_prefix,"")} : {position}")
        ms.squares[int(position[1])][int(position[0])].was_pressed(remote=True)

    
def on_disconnect(client, userdata, rc):
    global connected
    
    connected = False
    
if __name__ == "__main__":
    
    start_connect_window()
    client.disconnect()
    print("closed connection")