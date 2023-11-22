import tkinter as tk
from tkinter import font
import os

root = tk.Tk()

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

app = FullscreenApp(root)

exit_button = tk.Button(root, text="Exit", command=app.exit_app, font=custom_font)
exit_button.pack(expand=True)

root.mainloop()