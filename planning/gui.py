import tkinter as tk
from map import Map, Obstacle

root = tk.Tk()
root.geometry("700x700")
root.title("Planning Algorithms Testing")

size_x = 500
size_y = 500

canvas = tk.Canvas(root, width=size_x, height=size_y, border=None, background='white')
canvas.pack()

map = Map(size_x,size_y)
map.obstacles.append(Obstacle([[100,100],[100,300],[200,250]]))
map.obstacles.append(Obstacle([[450,400],[300,400],[100,450]]))

def draw_obstacle(obstacle: Obstacle):
    length = len(obstacle.vertices)
    for i in range(length):
        if i == length-1: # second to last element, circle back to start vertex
            canvas.create_line(obstacle.vertices[i][0], obstacle.vertices[i][1],obstacle.vertices[0][0],obstacle.vertices[0][1])
        else:
            canvas.create_line(obstacle.vertices[i][0], obstacle.vertices[i][1],obstacle.vertices[i+1][0],obstacle.vertices[i+1][1])


def update_obstacles(map: Map = map):
    for obstacle in map.obstacles:
        draw_obstacle(obstacle)
        
button = tk.Button(root,text="draw obstacles",command=update_obstacles)
button.pack()

root.mainloop() 
