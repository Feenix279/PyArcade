import tkinter as tk


def save_creds():
    file = open("creds.crd","w")
    file.write(f"{brokerentry.get()};{usrentry.get()};{pwentry.get()}")
    file.close()
    comlabel.config(text="Daten eingetragen! Bitte neustarten.")
    
root = tk.Tk()
root.title("Login Credentials")

comlabel = tk.Label(master=root, text="Hier bitte Logindaten eintragen")

brokerentry = tk.Entry(master=root)
usrentry = tk.Entry(master=root)
pwentry = tk.Entry(master=root, show="ඞ")

save_button = tk.Button(master=root, command=save_creds, text = "Speichern")


for i in [comlabel,brokerentry,usrentry,pwentry,save_button]:
    i.pack(anchor="center", padx=20, pady=10)




root.mainloop()
