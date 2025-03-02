import numpy as np
import tkinter as tk

STATES = {
    "EMPTY": 0,
    "FILLED": 1
}

COLORS = {
    0: 'white',
    1: 'black'
}

MODES = {
    "DRAW": 0,
    "PLACING_START": 1,
    "PLACING_GOAL": 2,
}

NODE_RADIUS = 2
HEIGHT = 30
WIDTH = 30
CELL_SIZE = 20
CURR_MODE = MODES["DRAW"]

START = None
GOAL = None

cost_map = np.zeros((HEIGHT, WIDTH))
root = tk.Tk()

def cost_map_clicked(event: tk.Event):

    # # print(f"{event.x},{event.y}")
    # if CURR_MODE == MODES["PLACING_GOAL"]:
    #     x0 = event.x 
    #     costmap_canvas.create_oval()
    
    if CURR_MODE == MODES["DRAW"]:
        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        cost_map[row, col] = STATES["FILLED"]
        update_canvas_cell(row, col)

def set_draw_mode():
    global CURR_MODE
    CURR_MODE = MODES["DRAW"]
    print(f"Set mode to DRAW {CURR_MODE}")
    
def set_place_start():
    global CURR_MODE
    CURR_MODE = MODES["PLACING_START"]
    print(f"Set mode to PLACING_START {CURR_MODE}")

def set_place_goal():
    global CURR_MODE
    CURR_MODE = MODES["PLACING_GOAL"]
    print(f"Set mode to PLACING_GOAL {CURR_MODE}") 

def update_canvas_cell(row, col):
    x1, y1 = col * CELL_SIZE, row * CELL_SIZE
    x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
    color = COLORS.get(cost_map[row, col])
    costmap_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

def update_canvas_costmap():
    for r in range(HEIGHT):
        for c in range(WIDTH):
            update_canvas_cell(r, c)
            
def run_algorithm():
    pass
            
costmap_canvas = tk.Canvas(root, height=HEIGHT * CELL_SIZE, width=WIDTH * CELL_SIZE)
costmap_canvas.pack()
costmap_canvas.bind("<Button-1>", cost_map_clicked)

button_frame = tk.Frame(root)
button_frame.pack()

draw_button = tk.Button(button_frame, command=set_draw_mode, text="Draw Mode")
draw_button.grid(row=1,column=1)

place_start_button = tk.Button(button_frame, command=set_place_start, text="Place Start Mode")
place_start_button.grid(row=1,column=2)

place_goal_button = tk.Button(button_frame, command=set_place_goal, text="Place Goal Mode")
place_goal_button.grid(row=1,column=3)

run_button = tk.Button(button_frame, command=run_algorithm, text="Run Algorithm")
run_button.grid(row=1,column=4)

update_canvas_costmap()
root.mainloop()
