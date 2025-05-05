import tkinter as tk
import paho.mqtt.client as mqtt
import random

class square():
    def __init__(self, x, y):
        self.isbomb = False
        self.bombcount = 0
        self.button = tk.Button(master=mainframe, height=2, width=4, text="", command=self.was_pressed, font="Arial 10 bold",bg="#6a797d", padx=0, pady=0, border=5)
        self.x = x
        self.y = y
        
    def was_pressed(self):
        if self.isbomb:
            end()
        else:
            self.button.config(text=str(self.bombcount), borderwidth=0, state="disabled")
            unsolved_squares.remove(self)
            self.button.config(state="disabled")
            if not unsolved_squares:
                end(True)
    def reveal(self):
        self.button.config(state="disabled")
        
        if self.isbomb:
            self.button.config(text = "B")
        else:
            self.button.config(text = str(self.bombcount))
    def set_color(self, overwrite = False):
        colors = ["#cccccc", "#ff6666", "#ffcc99", "#ccff99", "#99ffee",  "#99bbff", "#cc99ff", "#ff99dd", "#000"]
        self.button.config(fg=colors[self.bombcount], disabledforeground=colors[self.bombcount])
        
        if overwrite:
            self.button.config(fg=overwrite,disabledforeground=overwrite)

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
    
    conroot = tk.Tk()
    
    conroot.title("Verbinden")
    conroot.config(padx=15, pady=15)
    
    topic_text = tk.Label(conroot, text="Verbindungscode: ")
    topic_entry = tk.Entry(master=conroot)
    topic_button = tk.Button(master=conroot, text="Verbinden", command=connect)
    
    for i in [topic_text,topic_entry, topic_button]:
        i.pack(side="left", padx = 10)
        
    conroot.mainloop()
    def connect():
        global sub_topic
        sub_topic = "mindsweeper545158" + topic_entry.get()[8]
        mqtt_init()
        conroot.destroy()
        start_main_window()
        
    
def mqtt_disconnect ():
    client.disconnect()
    print("Verbindung getrennt")
    
def on_connect(client, userdata, flags, rc):
    global connected
    connected = True
    client.subscribe(sub_topic)
    
    print(f"Connected with result code {rc}")
    
def on_disconnect(client, userdata, rc):
    global connected
    
    connected = False
        
def on_message(client, userdata, msg):
    
    message = msg.payload.decode("utf-8")
    print(message)   
        
def start_main_window():
    global root
    global mainframe
    global resultlabel
    global size_input
    global bomb_input
    
    root = tk.Tk()
    root.config(bg="#3A4244")
    root.title("Minesweeper")
    
    menu = tk.Frame(master=root, bg="#3A4244")
    size_input = tk.Entry(master=menu)
    bomb_input = tk.Entry(master=menu)
    
    
    
    
    #vert_scroll = tk.Scrollbar(master = root)
    #hori_scroll = tk.Scrollbar(master = root)
    size_input.insert(0,"20x20")
    bomb_input.insert(0,"50")
    
    resultlabel = tk.Label(master = menu, fg="#FF0000", padx=15, bg="#3A4244")
    
    
    mainframe = tk.Frame(master=root, borderwidth=10, background="#3A4244")
    start_button = tk.Button(master=menu, command=create_grid, text="Starten")
    
    
    size_input.grid(row=1,column=1)
    bomb_input.grid(row=1,column=2)
    resultlabel.grid(row=1,column=3)
    start_button.grid(row=1,column=4)
    menu.pack()
    
    #vert_scroll.pack(side="right", fill="y")

    #hori_scroll.pack(side="bottom", fill="x")    
    
    mainframe.pack()

    root.mainloop()
    

def create_grid():
    
    global row_count
    global column_count
    global bomb_count
    global squares
    global unsolved_squares
    
    try:
        for r in squares:
            for c in r:
                c.button.destroy()
    except:
        pass
    row_count = int(size_input.get().split("x")[1])
    column_count = int(size_input.get().split("x")[0])
    if not row_count % 2 == 0 or not column_count % 2 == 0:
        return
    
    bomb_count = int(bomb_input.get())
    if not bomb_count or bomb_count>= row_count*column_count:
        return
    squares = []

    for r in range(0, row_count):
        columns = []
        for c in range(0, column_count):
            new_square = square(c,r)
            new_square.button.grid(row = r, column = c)
            columns.append(new_square)
        squares.append(columns)
    root.update()
    
    bombs = []
    bombs_placed = 0
    
    while bombs_placed < bomb_count:
        x = random.randint(0, column_count-1)
        y = random.randint(0, row_count-1)
        
        if not [x,y] in bombs:
            bombs.append([x,y])
            squares[y][x].isbomb = True
            bombs_placed += 1
    unsolved_squares = []
    for r in squares:
        for c in r:
            if not c.isbomb:
                local_bomb_count = 0
                
                y = squares.index(r)
                x = r.index(c)
                
                local_bomb_count += get_is_bomb(x-1,y-1)
                local_bomb_count += get_is_bomb(x,y-1)
                local_bomb_count += get_is_bomb(x+1,y-1)
                
                local_bomb_count += get_is_bomb(x-1,y)
                local_bomb_count += get_is_bomb(x+1,y)
                
                local_bomb_count += get_is_bomb(x-1,y+1)
                local_bomb_count += get_is_bomb(x,y+1)
                local_bomb_count += get_is_bomb(x+1,y+1)
                
                c.bombcount = local_bomb_count
                
                c.set_color()
                
                
                if not c.bombcount:
                    c.button.config(borderwidth=0, state="disabled")
                else:
                    unsolved_squares.append(c)
            else:
                c.set_color("#ff4d4d")
                          
def get_is_bomb(x,y):
    
    if x >= 0 and x <= column_count-1 and y >= 0 and y <= row_count-1:
        
        if squares[y][x].isbomb:
            return 1
        else:
            return 0
    else:
        return 0

def end(good_ending = False):
    if not good_ending:
        resultlabel.config(text="Verloren!")
    else:
        resultlabel.config(text="Gewonnen!", fg="#0F0")
    for r in squares:
        for c in r:
            c.reveal()
    
if __name__ == "__main__":    
    start_connect_window()