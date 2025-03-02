'''
Rapidly Exploring Random Trees (2001)


1. start node
2. randomly place node anywhere in the state space
3. connect node to nearest node in tree
        specify a max distance new node can be from nearest node
        if new node is closer than max distance, just choose new node
        is there is an obstacle between nearest node and where new node is placed, ignore completely

4. when the path is within some threshold of goal, have a viable path

lets make a map and a way to draw in it

'''

import numpy as np
import tkinter as tk

