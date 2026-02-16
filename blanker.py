#!/usr/bin/env python3
import tkinter as tk
import os
import sys

class UniversalBlanker:
    def __init__(self):
        # Ensure the script knows which display to use (standard for Linux is :0)
        if "DISPLAY" not in os.environ:
            os.environ["DISPLAY"] = ":0"
            
        try:
            self.root = tk.Tk()
        except tk.TclError:
            # If :0 fails, try to grab the current user's display
            print("Could not connect to display :0, exiting.")
            sys.exit(1)
        
        # 1. Screen Dimensions
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        
        # 2. Setup Window
        self.root.overrideredirect(True) 
        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.configure(background='black')
        self.root.attributes('-topmost', True)
        self.root.config(cursor="none")

        # 3. State Management
        self.last_mouse_pos = None
        self.ready_to_exit = False
        self.root.after(500, self.enable_exit)

        # 4. Bindings
        self.root.bind('<Any-KeyPress>', self.exit_app)
        self.root.bind('<Button-1>', self.exit_app)
        self.root.bind('<Motion>', self.handle_mouse)
        self.root.bind('<Escape>', self.exit_app)

        self.root.mainloop()

    def enable_exit(self):
        self.ready_to_exit = True

    def handle_mouse(self, event):
        if not self.ready_to_exit: return
        if self.last_mouse_pos is None:
            self.last_mouse_pos = (event.x, event.y)
            return
        dx = abs(event.x - self.last_mouse_pos[0])
        dy = abs(event.y - self.last_mouse_pos[1])
        if dx > 10 or dy > 10:
            self.exit_app()

    def exit_app(self, event=None):
        self.root.destroy()

if __name__ == "__main__":
    UniversalBlanker()
