import random, time, math
import numpy as np 
import tkinter as tk
from typing import Callable
from os import system, name


def clear_terminal_output():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


class Maze:

    DEFAULT_PIXELS_PER_MAZE_CELL = 20

    UNPOPULATED = 0
    POPULATED = 1
    GOAL = 3
    ROBOT = 4 
    PATH = 5
    ROBOT_AT_GOAL = 6

    COLORS = {
        UNPOPULATED: '#ffffff',
        POPULATED: '#757575',
        GOAL: '#cc0000',
        ROBOT: '#6a7b8b',
        PATH: '#c0d7ec',
        ROBOT_AT_GOAL: '#9B3E46',
    }

    DEFAULT_WINDOW_WIDTH_PX = 1000

    def __init__(self, size: int, algorithm_to_run: Callable, gui_title: str):

        clear_terminal_output()

        def algorithm_runner_wrapper(algorithm_to_run):
            self.run_algorithm_button.config(state=tk.DISABLED)
            try:
                algorithm_to_run()
            except Exception as exception:
                print(exception)
                print("To restart, close the maze window")

        
        def _depth_first_search_maze(x, y) -> None:
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)] # ensures pathways between walls
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.maze_state[nx, ny] == self.POPULATED:
                    # Mark the cell between the current cell and the next cell as UNPOPULATED
                    self.maze_state[x + dx // 2][y + dy // 2] = self.UNPOPULATED
                    self.maze_state[nx, ny] = self.UNPOPULATED
                    _depth_first_search_maze(nx, ny)


        # maze initialization
        self.size = size
        self.rectangles = {}

        self.maze_state = np.full((size, size), self.POPULATED)
        _depth_first_search_maze(0,0)

        self.DEFAULT_PIXELS_PER_MAZE_CELL = math.ceil(self.DEFAULT_WINDOW_WIDTH_PX / self.size)

        # gui Initialization
        self.maze_gui = tk.Tk(); self.maze_gui.title(gui_title)
        # making gui frame for maze cells
        self.frame = tk.Frame(self.maze_gui); self.frame.pack(pady=10, padx=10)
        # making button to run algorithm
        self.run_algorithm_button = tk.Button(self.maze_gui, text="Run Algorithm", command= lambda: algorithm_runner_wrapper(algorithm_to_run)); self.run_algorithm_button.config(state=tk.DISABLED); self.run_algorithm_button.pack()
        # making canvas for gui
        self.canvas = tk.Canvas(self.frame, width=self.size * self.DEFAULT_PIXELS_PER_MAZE_CELL, height=self.size * self.DEFAULT_PIXELS_PER_MAZE_CELL); self.canvas.pack()
        # making speed slider that wil adjust the timesteps of the visualization of the algorithms
        self.speed_slider = tk.Scale(self.frame, from_=1, to=100, orient=tk.HORIZONTAL, label="Speed multiplier"); self.speed_slider.set(1); self.speed_slider.pack(fill=tk.X)

        self.update_gui()


    def update_gui(self) -> None:
        unit_size = self.DEFAULT_PIXELS_PER_MAZE_CELL
        for row in range(self.size):
            for col in range(self.size):
                x1, y1, x2, y2 = col * unit_size, row * unit_size, col * unit_size + unit_size, row * unit_size + unit_size
                cell_value = self.maze_state[row, col]
                if (row, col) not in self.rectangles:
                    self.rectangles[(row, col)] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.COLORS[cell_value], outline="black")
                else:
                    self.canvas.itemconfig(self.rectangles[(row, col)], fill=self.COLORS[cell_value])
        self.maze_gui.update()

    def _make_empty(self):
        self.maze_state = np.zeros((self.size,self.size))

class Robot():

    DEFAULT_LOAD_DELAY_SEC = 0.2
    DEFAULT_MOVEMENT_TIME_STEP_SEC = 0.1

    def _is_valid_position(self, proposed_position: tuple[int]) -> bool:
        return all([0 <= coord < self.maze.size for coord in proposed_position]) and (len(proposed_position) == 2)
    

    def _is_free_space(self, proposed_position: tuple[int]) -> bool:
        return (self.maze.maze_state[proposed_position] != self.maze.POPULATED)
    

    def _is_valid_movement(self, proposed_position) -> bool:
        return self._is_free_space(proposed_position) and self._is_valid_position(proposed_position)
    

    def _update_maze_gui(self, updated_position: tuple[int], updated_maze_state):
        if self._is_valid_position(updated_position):
            self.maze.maze_state[updated_position] = updated_maze_state
            self.maze.update_gui()
        else:
            raise ValueError(f"The value of the updated maze position {updated_position} is not within the maze")


    def __init__(self, maze: Maze, start_position: tuple[int], goal_position: tuple[int]):

        def _load_delay():
            time.sleep(self.DEFAULT_LOAD_DELAY_SEC)

        self.maze = maze
        self.at_goal = False
        
        # checking if the start position of the robot is within the maze
        if self._is_valid_position(start_position): self.start_position = start_position
        else: raise ValueError(f"The start position of the robot {start_position} is not within it's maze")
        
        # checking if the goal position of the robot is within the maze
        if self._is_valid_position(goal_position): self.goal_position = goal_position
        else: raise ValueError(f"The goal position of the robot {goal_position} is not within it's maze")

        # if we have gotten here, the start position is valid, make it the current position
        self.current_position = start_position

        _load_delay()
        self._update_maze_gui(self.goal_position, self.maze.GOAL)

        _load_delay()
        self._update_maze_gui(self.current_position, self.maze.ROBOT)

        self.maze.run_algorithm_button.config(state=tk.NORMAL)


    def _move(self, movement_delta: tuple[int]) -> bool:

        proposed_new_position = tuple(map(sum, zip(self.current_position, movement_delta)))

        if self._is_valid_movement(proposed_new_position): 

            old_position = self.current_position
            self.current_position = proposed_new_position

            time.sleep( self.DEFAULT_MOVEMENT_TIME_STEP_SEC /(self.maze.speed_slider.get()))

            if old_position == self.start_position:
                self._update_maze_gui(old_position, self.maze.PATH)
            else:
                self._update_maze_gui(old_position, self.maze.PATH)

            # check if current position is goal, if so set "at goal" 
            if self.current_position == self.goal_position:

                self.at_goal = True
                self._update_maze_gui(self.current_position,self.maze.ROBOT_AT_GOAL)
                print("\nThe robot has reached the goal\n")

            else:
                self._update_maze_gui(self.current_position,self.maze.ROBOT)

        else: 
            raise ValueError(f"The proposed movement of the robot {movement_delta} is not valid given the robot's current position {self.current_position}")
        
    def move_right(self):
        self._move((0,1))

    def move_left(self):
        self._move((0,-1))

    def move_down(self):
        self._move((1,0))

    def move_up(self):
        self._move((-1,0))


def main():

    def example_algorithm():
        while not robot.at_goal:
            robot.move_down()
            robot.move_right()
            
    part1_maze_size = 11

    maze = Maze(part1_maze_size, example_algorithm, "Part 1")
    maze._make_empty()
    robot = Robot(maze,(0,0),(part1_maze_size - 1, part1_maze_size - 1))
    maze.maze_gui.mainloop()

if __name__ == '__main__':
    main()