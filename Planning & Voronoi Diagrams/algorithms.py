import numpy as np
import matplotlib.pyplot as plt
from heapq import heappop, heappush

# A* function definition (your previous code here)
def a_star(cost_map, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(node, rows, cols):
        x, y = node
        neighbors = []
        if x > 0: neighbors.append((x - 1, y))
        if x < rows - 1: neighbors.append((x + 1, y))
        if y > 0: neighbors.append((x, y - 1))
        if y < cols - 1: neighbors.append((x, y + 1))
        return neighbors

    rows, cols = cost_map.shape
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = np.full((rows, cols), np.inf, dtype=np.float32)
    g_score[start] = 0
    f_score = np.full((rows, cols), np.inf, dtype=np.float32)
    f_score[start] = heuristic(start, end)

    while open_set:
        _, current = heappop(open_set)
        if current == end:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path

        for neighbor in get_neighbors(current, rows, cols):
            tentative_g_score = g_score[current] + cost_map[neighbor]
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heappush(open_set, (f_score[neighbor], neighbor))

    return []