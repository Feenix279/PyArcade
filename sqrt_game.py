import tkinter as tk
import random
import math

def create_window():
    global random_toggle
    global stage_toggle

    random_toggle = True
    stage_toggle = False
    
    def exinp_func():
        square = random_entry.get()
        try:
            square = int(square)
        except ValueError:
            return
        resutlabel.config(text=f"Ergebnis: {str(math.sqrt(square))}")

    def random_func():
        global square
        global stage_toggle

        if not stage_toggle:
            range = random_entry.get()
            range_max = range.split("-")[1]
            range_min = range.split("-")[0]
            print("war hier")
            try:
                range_max = int(range_max)
                range_min = int(range_min)
            except ValueError:
                return
        
            square = random.randrange(range_min,range_max, 1)
            resutlabel.config(text=f"Zahl: {square}")
            stage_toggle = True
        else:
            resutlabel.config(text=f"Ergebnis: {str(math.sqrt(square))}")
            stage_toggle = False

    def rand_toggle():
        global random_toggle
        if random_toggle:
            random_button.config(command=exinp_func)
            resutlabel.config(text="Exact Input")
            random_toggle = False
        else:
            random_button.config(command=random_func)
            resutlabel.config(text="Range Input")
            random_toggle = True

    random_toggle = True

    root = tk.Tk()
    root.title("sqrt game")


    resutlabel = tk.Label(master=root, text="Range input")
    toggle_button = tk.Button(master=root, command=rand_toggle, text="Toggle")
    resutlabel.pack(padx=20, pady=15)



    random_frame = tk.Frame(root)
    random_button = tk.Button(master=random_frame, text="Calculate", command=random_func)
    random_entry = tk.Entry(master=random_frame)
    random_frame.pack(padx=20,pady=20)
    random_button.pack(side="right", padx=10)
    random_entry.pack(side="left", padx=10)

    toggle_button.pack(anchor="center", pady=25)
    root.mainloop()



if __name__ == "__main__":
    create_window()