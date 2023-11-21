import tkinter as tk
from tkinter import font
import os

root = tk.Tk()

custom_font = font.Font(family="Helvetica", size=20, weight="bold")
class FullscreenApp:
    def __init__(self, master, **kwargs):
        self.master = master
        master.attributes('-fullscreen', True)
        master.bind('<Escape>', self.toggle_fullscreen)
        master.bind('<Button-1>', self.exit_app)

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_app, font=custom_font)
        self.exit_button.pack(expand=True)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.master.attributes('-fullscreen', self.state)

    def exit_app(self, event=None):
        self.master.destroy()

app = FullscreenApp(root)

root.mainloop()