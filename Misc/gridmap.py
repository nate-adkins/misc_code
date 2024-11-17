import math, random, time, contextlib, operator

class Cell():


    def __init__(self, state: bool, occupied: int, x: int, y: int):
        self._infinite_cost: int = 100

        self.x: int = x
        self.y: int = y
        self.occupied: int = occupied
        self.state: bool = state
        self.cost: int = self._infinite_cost
        self.parent: Cell 


class Map():


    def __str__(self, map_type: str):
        if not isinstance(map_type, str):
            raise TypeError('map_type must be a string')
        map_attribute = operator.attrgetter(map_type)
        output = ""
        for cell_row in self.map:
            output += str([ map_attribute(cell) for cell in cell_row]) + "\n"
        return(output)


    def __init__(self, size: int, occupation_density: float):
        self.size: int = size
        self.occupation_density: float = occupation_density 
        self.map: list[list[Cell]] = self._populate_map()
        print(f"\nMade the map:\n\n{self.__str__('occupied')}")


    def _populate_map(self):
        new_map = [ [Cell(False, 0, x, y) for x in range(self.size)] for y in range(self.size) ]

        unique_positions = math.ceil((self.size**2) * self.occupation_density)
        x_positions = [ random.randint(0,self.size - 1) for _ in range(unique_positions)]
        y_positions = [ random.randint(0,self.size - 1) for _ in range(unique_positions)]

        for x,y in zip(x_positions,y_positions):
            new_map[y][x].occupied = 1
        return new_map


class timer_decorator(contextlib.ContextDecorator):
    def __enter__(self):
        self.rel_time = time.time_ns()
        return self
    def __exit__(self, *exc):
        print(f"Algorithm took: {(time.time_ns() - self.rel_time)/1e9} seconds")
        return False


@timer_decorator()
def dijkstra(input_map: Map, start: tuple, end: tuple):

    CLOSED: bool = False
    OPEN: bool = True 
    INFINITE_COST: int = 100

    # Initalizing maps 
    cost_map: list[list[int]] = [ [INFINITE_COST] for _ in range(input_map.size) for __ in range(input_map.size)]
    state_map: list[list[bool]] = [ [CLOSED] * input_map.size for _ in range(input_map.size)]

    # Initializing starting cell 
    cost_map[start(0)][start(1)] = 0 
    state_map[start(0)][start(1)] = OPEN 

    def update_adjacent_vertices(curr_x: int, curr_y: int):
        rel_pos = [ (-1, 1) , (0, 1), (1, 1),
                    (-1, 0) ,         (1, 0),
                    (-1,-1) , (0,-1), (1,-1),
                  ]
        
        mvmt_cost = [ 14, 10, 14, 
                      10,     10, 
                      14, 10, 14,
                    ]
        
        for x,y, cost in zip(rel_pos, mvmt_cost):
            new_x = curr_x + x
            new_y = curr_y + y
            for val in [new_x, new_y]:
                if (val >= input_map.size or val < 0):
                    continue
            cost_map[new_x][new_y] = cost_map[curr_x][curr_y] + cost

        
    pass


def main():
    map = Map(10, 0.30)
    dijkstra(map,(0,0),(9,9))


if __name__ == '__main__':
    main()