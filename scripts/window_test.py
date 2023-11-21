import tkinter as tk
from tkinter import font
import os
 
current_dir = os.path.dirname(os.path.abspath(__file__))  
parent_dir = os.path.dirname(current_dir)  
fonts_folder = os.path.join(parent_dir, 'fonts')
font_display1_path = os.path.join(fonts_folder, 'display1.otf')

font_display1 = font.Font(family="Display 1", file=font_display1_path, size=24)

class FullscreenApp:
    def __init__(self, master, **kwargs):
        self.master = master
        master.attributes('-fullscreen', True)
        master.bind('<Escape>', self.toggle_fullscreen)
        master.bind('<Button-1>', self.exit_app)

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_app, font=font_display1)
        self.exit_button.pack(expand=True)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.master.attributes('-fullscreen', self.state)

    def exit_app(self, event=None):
        self.master.destroy()

root = tk.Tk()
app = FullscreenApp(root)
root.mainloop()

# Create a temporary Tkinter root window
root = tk.Tk()

# List all available font families
font_list = font.families()
for font_family in font_list:
    print(font_family)

# Close the temporary root window
root.destroy()