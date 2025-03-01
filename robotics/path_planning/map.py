'''
What I want to build

dijkstras
A*
RRT
RRT*

Need:

way to store a grid map with 0-1 cost values in the map
maybe want a way to generate random terrain
want a way to draw terrain

'''
import random
from math import pi, cos, sin
def random_vector():
    theta = random.uniform(0,2*pi)
    return (cos(theta), sin(theta))

def perlin_noise():
    
    # make grid
    # for each cell, make a random vector with unit length
    # 
    
    pass


print(random_vector())