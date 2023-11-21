import tkinter as tk
from tkinter import font
from tkinter import ttk
import os

root = tk.Tk()

custom_font = font.Font(family="Quicksand", size=20, weight="bold")

class RoundedButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        ttk.Button.__init__(self, master, **kwargs)

        # Configure the button style to have rounded corners
        self.style = ttk.Style()

        self.style.configure(
            'RoundedButton.TButton',
            borderwidth=5,
            relief="flat",
            bordercolor="gray",
            background="lightgray",
            foreground="black",
            padding=10,
            font=('Helvetica', 12)
        )

        self.configure(style='RoundedButton.TButton')

class FullscreenApp:
    def __init__(self, master, **kwargs):
        self.master = master
        master.attributes('-fullscreen', True)
        master.bind('<Escape>', self.toggle_fullscreen)
        master.bind('<Button-1>', self.exit_app)

        self.exit_button = RoundedButton(master, text="Exit", command=self.exit_app, font=custom_font)
        self.exit_button.pack(expand=True)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.master.attributes('-fullscreen', self.state)

    def exit_app(self, event=None):
        self.master.destroy()

app = FullscreenApp(root)

root.mainloop()