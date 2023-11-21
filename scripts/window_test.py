import tkinter as tk
from tkinter import font

class FullscreenApp:
    def __init__(self, master, **kwargs):
        self.master = master
        master.attributes('-fullscreen', True)
        master.bind('<Escape>', self.toggle_fullscreen)
        master.bind('<Button-1>', self.exit_app)

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_app)
        self.exit_button.pack(expand=True)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.master.attributes('-fullscreen', self.state)

    def exit_app(self, event=None):
        self.master.destroy()

root = tk.Tk()
app = FullscreenApp(root)
root.mainloop()

font_list = font.families()
for font_family in font_list:
    print(font_family)
