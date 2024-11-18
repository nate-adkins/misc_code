import tkinter as tk
import numpy as np
from numpy.typing import NDArray
from algorithms import a_star

CANVAS_BLANK = "#ffffff"
BACKGROUND = "#b0ffb0"
BUTTON_COLOR = "#ffffff"
BUTTON_HOVER_COLOR = "#10ff10"

COLORS = {
    0: CANVAS_BLANK,  # Blank cell
    1: "#000000",     # Obstacle
    2: "#00ff00",     # Start (green)
    3: "#0000ff",     # End (blue)
    4: "#ff0000"      # Path (red)
}

class MapGUI:
    def __init__(self, root: tk.Tk):
        self.cell_size = 50
        self.map_size = 1000
        self.cells: NDArray[np.int8] = np.zeros((self.map_size // self.cell_size, self.map_size // self.cell_size), dtype=np.int8)
        self.start_point = None
        self.end_point = None
        self.last_canvas_right_click_x_y = None

        self.root = root
        root.resizable(False, False)
        self.root.title("Planner")
        root.configure(bg=BACKGROUND)
        
        self.controls_frame = tk.Frame(root, width=10, height=100)
        self.controls_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="n")

        self.options_label1 = tk.Label(self.controls_frame, width=10, height=4, bg=BUTTON_COLOR, text="Options", highlightbackground=BUTTON_HOVER_COLOR, activebackground=BUTTON_HOVER_COLOR)
        self.options_label1.grid(row=0, column=0)
        self.options_label1.bind("<Button-3>", self.on_label1_click)
        
        self.options_context_menu = tk.Menu(self.root, tearoff=0)
        self.options_context_menu.add_command(label="Save map as csv")
        self.options_context_menu.add_command(label="Load map from csv")
        self.options_context_menu.add_separator()
        self.options_context_menu.add_command(label="Clear current map", command=self.clear_map)
        
        self.canvas = tk.Canvas(self.root, width=self.map_size, height=self.map_size, bg=CANVAS_BLANK, border=0, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=0, column=1, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Button-3>", self.canvas_right_click)

        self.canvas_context_menu = tk.Menu(self.root, tearoff=0)
        self.canvas_context_menu.add_command(label="Add start", command=self.set_start)
        self.canvas_context_menu.add_command(label="Add end", command=self.set_end)
        self.canvas_context_menu.add_separator()
        self.canvas_context_menu.add_command(label="Remove path", command=self.remove_path)

    def update_cell(self, x_index, y_index, state):
        self.cells[y_index][x_index] = state
        canvas_x, canvas_y = x_index * self.cell_size, y_index * self.cell_size
        color = COLORS[state]
        self.canvas.create_rectangle(canvas_x, canvas_y, canvas_x + self.cell_size, canvas_y + self.cell_size, fill=color, outline="")

    def on_label1_click(self, event):
        self.options_label1.config(background=BUTTON_HOVER_COLOR)
        self.options_context_menu.post(event.x_root, event.y_root)
        self.options_label1.config(background=BUTTON_COLOR)
    
    def canvas_click(self, event):
        x_index = event.x // self.cell_size
        y_index = event.y // self.cell_size
        self.update_cell(x_index, y_index, 1)
        
    def canvas_right_click(self, event):
        self.canvas_context_menu.post(event.x_root, event.y_root)
        self.last_canvas_right_click_x_y = event.x, event.y

    def set_start(self):
        if self.last_canvas_right_click_x_y:
            x_index = self.last_canvas_right_click_x_y[0] // self.cell_size
            y_index = self.last_canvas_right_click_x_y[1] // self.cell_size
            self.start_point = (y_index, x_index)
            self.update_cell(x_index, y_index, 2) 
            self.run_a_star()

    def set_end(self):
        if self.last_canvas_right_click_x_y:
            x_index = self.last_canvas_right_click_x_y[0] // self.cell_size
            y_index = self.last_canvas_right_click_x_y[1] // self.cell_size
            self.end_point = (y_index, x_index)
            self.update_cell(x_index, y_index, 3)
            self.run_a_star()

    def remove_path(self):
        if self.start_point and self.end_point:
            self.update_cell(self.end_point[1], self.end_point[0], 0)
            self.update_cell(self.start_point[1], self.start_point[0], 0) 
            self.start_point, self.end_point = None, None
            self.clear_path()

    def run_a_star(self):
        if self.start_point and self.end_point:
            path = a_star(self.cells, self.start_point, self.end_point)
            for (y, x) in path:
                self.update_cell(x, y, 4) 

    def clear_path(self):
        for row in range(self.cells.shape[0]):
            for col in range(self.cells.shape[1]):
                if self.cells[row, col] == 4:  
                    self.update_cell(col, row, 0)

    def clear_map(self):
        self.cells.fill(0)
        self.canvas.delete("all")

def main():
    root = tk.Tk()
    app = MapGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
