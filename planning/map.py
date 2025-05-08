class Obstacle():
    
    def __init__(self, vertices: list[list[int]]):
        self.vertices = vertices

class Map():
    
    def __init__(self, max_x, max_y):
        self.obstacles: list[Obstacle] = []
        self.max_x: int = max_x
        self.max_y: int = max_y
        