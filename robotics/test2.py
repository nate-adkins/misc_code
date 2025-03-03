import numpy as np
import tkinter as tk
import random
import math
from PIL import Image, ImageTk

STATES = {
    "EMPTY": 5,  # Free space is now represented by 5
    "FILLED": 1
}

COLORS = {
    0: 'white',
    1: 'black',
    2: 'blue',  # Start node
    3: 'red',   # Goal node
    4: 'green'  # Path nodes
}

MODES = {
    "DRAW": 0,
    "PLACING_START": 1,
    "PLACING_GOAL": 2,
}

NODE_RADIUS = 3
HEIGHT = 600
WIDTH = 600
CURR_MODE = MODES["DRAW"]

START = None
GOAL = None

cost_map = np.zeros((HEIGHT, WIDTH))
nodes = []
edges = {}
root = tk.Tk()
root.title("RRT running on USGS slope map (White are areas with >30 degrees slope)")

Image.MAX_IMAGE_PIXELS = None
image = Image.open("map.png").convert("L").resize((WIDTH, HEIGHT))
cost_map = np.array(image)

cost_map = (cost_map == STATES["EMPTY"])  

background_image = ImageTk.PhotoImage(image)

def cost_map_clicked(event: tk.Event):
    global START, GOAL
    x, y = event.x, event.y
    
    if CURR_MODE == MODES["PLACING_START"]:
        START = (x, y)
    elif CURR_MODE == MODES["PLACING_GOAL"]:
        GOAL = (x, y)
    update_canvas()

def update_canvas():
    costmap_canvas.delete("all")
    costmap_canvas.create_image(0, 0, anchor=tk.NW, image=background_image)
    
    for node, parent in edges.items():
        costmap_canvas.create_line(node[0], node[1], parent[0], parent[1], fill="green")
    for node in nodes:
        costmap_canvas.create_oval(node[0] - NODE_RADIUS, node[1] - NODE_RADIUS, 
                                   node[0] + NODE_RADIUS, node[1] + NODE_RADIUS, fill="green")
    if START:
        costmap_canvas.create_oval(START[0] - NODE_RADIUS, START[1] - NODE_RADIUS, 
                                   START[0] + NODE_RADIUS, START[1] + NODE_RADIUS, fill="blue")
    if GOAL:
        costmap_canvas.create_oval(GOAL[0] - NODE_RADIUS, GOAL[1] - NODE_RADIUS, 
                                   GOAL[0] + NODE_RADIUS, GOAL[1] + NODE_RADIUS, fill="red")

def run_rrt_star():
    if not START or not GOAL:
        print("Start and Goal must be set!")
        return
    
    nodes.clear()
    edges.clear()
    nodes.append(START)
    animate_rrt()

# Add this function to increment iterations
def add_more_iterations():
    animate_rrt(iteration=len(nodes), additional_iterations=100)

# Modify the existing `animate_rrt` function
current_iteration = 0
max_iterations = 1000

def run_rrt_star():
    """Start RRT* pathfinding from scratch."""
    global current_iteration, max_iterations
    if not START or not GOAL:
        print("Start and Goal must be set!")
        return

    nodes.clear()
    edges.clear()
    nodes.append(START)
    current_iteration = 0
    max_iterations = 1000  # Initial run starts with 1000 iterations
    animate_rrt()

def add_more_iterations():
    """Add 100 iterations to the running RRT* process."""
    global max_iterations
    max_iterations += 1000
    animate_rrt()

def animate_rrt():
    """Perform RRT* iterations."""
    global current_iteration

    if current_iteration >= max_iterations:
        draw_path()
        return

    rand_node = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
    if not cost_map[rand_node[1], rand_node[0]]:  # Check for free space
        current_iteration += 1
        root.after(1, animate_rrt)
        return
    
    nearest_node = min(nodes, key=lambda n: math.dist(n, rand_node))
    new_node = step_towards(nearest_node, rand_node)
    if not cost_map[new_node[1], new_node[0]]:  # Check for free space
        current_iteration += 1
        root.after(1, animate_rrt)
        return

    nodes.append(new_node)
    edges[new_node] = nearest_node
    update_canvas()
    
    current_iteration += 1
    if math.dist(new_node, GOAL) < 10:
        edges[GOAL] = new_node
        draw_path()
        return

    root.after(10, animate_rrt)

def step_towards(start, end, step_size=10):
    vec = (end[0] - start[0], end[1] - start[1])
    length = math.hypot(*vec)
    if length < step_size:
        return end
    direction = (vec[0] / length, vec[1] / length)
    new_node = (round(start[0] + direction[0] * step_size), round(start[1] + direction[1] * step_size))
    return new_node if 0 <= new_node[0] < WIDTH and 0 <= new_node[1] < HEIGHT else start

def draw_path():
    node = GOAL
    while node in edges:
        parent = edges[node]
        costmap_canvas.create_line(node[0], node[1], parent[0], parent[1], fill="red", width=2)
        node = parent
    update_canvas()

def clear_canvas():
    """Clear all nodes, edges, and start/goal positions."""
    global START, GOAL, nodes, edges
    START = None
    GOAL = None
    nodes.clear()
    edges.clear()
    update_canvas()

    

costmap_canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
costmap_canvas.pack()
costmap_canvas.bind("<Button-1>", cost_map_clicked)

button_frame = tk.Frame(root)
button_frame.pack()

draw_button = tk.Button(button_frame, command=lambda: set_mode("DRAW"), text="Draw Mode")
draw_button.grid(row=1, column=1)

place_start_button = tk.Button(button_frame, command=lambda: set_mode("PLACING_START"), text="Place Start")
place_start_button.grid(row=1, column=2)

place_goal_button = tk.Button(button_frame, command=lambda: set_mode("PLACING_GOAL"), text="Place Goal")
place_goal_button.grid(row=1, column=3)

run_button = tk.Button(button_frame, command=run_rrt_star, text="Run RRT")
run_button.grid(row=1, column=4)

add_iterations_button = tk.Button(button_frame, command=add_more_iterations, text="Add 1000 Iterations")
add_iterations_button.grid(row=1, column=5)

clear_button = tk.Button(button_frame, command=clear_canvas, text="Clear")
clear_button.grid(row=1, column=6)


def set_mode(mode):
    global CURR_MODE
    CURR_MODE = MODES[mode]
    print(f"Set mode to {mode}")

update_canvas()
root.mainloop()
