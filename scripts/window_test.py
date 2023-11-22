import tkinter as tk
from tkinter import font
import os

root = tk.Tk()
root.geometry("800x480")

custom_font = font.Font(family="Quicksand", size=20, weight="bold")

class FullscreenApp:
    def __init__(self, master, **kwargs):
        self.master = master
        master.attributes('-fullscreen', True)
        master.bind('<Escape>', self.toggle_fullscreen)
        master.bind('<Button-1>', self.exit_app)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.master.attributes('-fullscreen', self.state)

    def exit_app(self, event=None):
        self.master.destroy()

class ToggleButton(tk.Button):
    def __init__(self, master, on_toggle_on=None, on_toggle_off=None, **kwargs):
        super().__init__(master, **kwargs)
        self.var = tk.BooleanVar(False)
        
        self.config(relief=tk.RAISED)
        
        self.bind("<ButtonPress-1>", self.on_tap)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        self.on_toggle_on = on_toggle_on
        self.on_toggle_off = on_toggle_off
        
    def on_tap(self, event):
        self.var.set(True)
        self.config(relief=tk.SUNKEN)
        if self.on_toggle_on is not None:
            self.on_toggle_on()

    def on_release(self, event):
        self.var.set(False)
        self.config(relief=tk.RAISED) 
        if self.on_toggle_off is not None:
            self.on_toggle_off()

app = FullscreenApp(root)

exit_button = tk.Button(root, text="Exit", command=app.exit_app, font=custom_font)
exit_button.place(relx=0.5, rely=0.5, anchor=tk.W, width=200, height=100)

toggle_button = ToggleButton(root, text="Toggle", font=custom_font)
toggle_button.place(relx=0.5, rely=0.5, anchor=tk.E, width=200, height=100)

root.mainloop()