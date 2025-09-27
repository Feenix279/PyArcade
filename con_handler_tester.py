import connection_handler as ch
import tkinter as tk
import time
    
def timeouted(missing:str, cleared:bool = False):
    pass
        
def init(data:str=None):
    if not data:
        #generate data
        data = "random string"

    print(f"Init data: {data}")
    return data

def event(missing):
    print("received event")

def received_move(move):
    print(f"Receiver move {move}")
        
if __name__ == "__main__":
    handler = ch.default_ui(init, received_move, event, timeouted)
    while True:
        time.sleep(1)
