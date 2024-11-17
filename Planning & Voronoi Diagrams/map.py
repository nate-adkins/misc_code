import tkinter as tk
import numpy as np
from numpy.typing import NDArray
import random, math

CANVAS_BLANK = "#ffffff"
BACKGROUND = "#b0ffb0"

BUTTON_COLOR = "#ffffff"
BUTTON_HOVER_COLOR = "#10ff10"

def convert_to_hex(value):
    if(0x00 <= value <= 0xFF): return '#' + f'{0xFF - value:02x}'*3 
    else: raise ValueError("Input must be an integer between 0 and 255")
    
class MapGUI:
    def __init__(self, root: tk.Tk):
        
        self.cell_size = 50
        self.map_size = 1000
        
        self.cells: NDArray[np.int8] = np.zeros((self.map_size//self.cell_size,self.map_size//self.cell_size),dtype=np.uint8)
                
        self.root = root
        root.resizable(False, False)
        self.root.title("Planner")
        root.configure(bg=BACKGROUND)
        
        self.controls_frame = tk.Frame(root, width=10, height=100)
        self.controls_frame.grid(row=0, column=0, padx=(10,0), pady=10, sticky="n")

        self.options_label1 = tk.Label(self.controls_frame, width=10, height=4, bg=BUTTON_COLOR,text="options",highlightbackground=BUTTON_HOVER_COLOR, activebackground=BUTTON_HOVER_COLOR)
        self.options_label1.grid(row=0, column=0)
        self.options_label1.bind("<Button-3>",self.on_label1_click)
        
        self.options_context_menu = tk.Menu(self.root, tearoff=0)
        self.options_context_menu.add_command(label="Save map as csv",)
        self.options_context_menu.add_command(label="Load map from csv",)
        self.options_context_menu.add_separator()
        self.options_context_menu.add_command(label="Clear current map",)
        
        self.canvas = tk.Canvas(self.root, width=self.map_size, height=self.map_size, bg=CANVAS_BLANK, border=0, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=0, column=1, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Button-3>",self.canvas_right_click)

        self.canvas_context_menu = tk.Menu(self.root, tearoff=0)
        
        self.canvas_context_menu.add_command(label="Clear cell",command=self.clear_cell)
        self.canvas_context_menu.add_separator()
        self.canvas_context_menu.add_command(label="Add start",)
        self.canvas_context_menu.add_command(label="Add end",)
        self.canvas_context_menu.add_separator()
        self.canvas_context_menu.add_command(label="Remove start",)
        self.canvas_context_menu.add_command(label="Remove end",)
        
    def update_cell(self, x_index, y_index, color):
        self.cells[x_index][y_index] = color
        canvas_x, canvas_y= (x_index) * self.cell_size, (y_index) * self.cell_size

        self.canvas.create_rectangle(canvas_x, canvas_y, canvas_x + self.cell_size, canvas_y + self.cell_size, fill=convert_to_hex(color), outline="")


    def on_label1_click(self,event): self.options_label1.config(background=BUTTON_HOVER_COLOR); self.options_context_menu.post(event.x_root, event.y_root); self.options_label1.config(background=BUTTON_COLOR)
    
    def canvas_click(self, event):
        val = math.floor(random.random() * 255)
        x_index = (event.x // self.cell_size)
        y_index = (event.y // self.cell_size)
        self.update_cell(x_index,y_index, val)
        
    def clear_cell(self,event):
        x_index = (event.x // self.cell_size)
        y_index = (event.y // self.cell_size)
        self.update_cell(x_index,y_index, 0) 
        
    def canvas_right_click(self, event):
        self.canvas_context_menu.post(event.x_root, event.y_root)

def main():
    root = tk.Tk()
    app = MapGUI(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()