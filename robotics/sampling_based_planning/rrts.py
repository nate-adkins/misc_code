'''
Rapidly Exploring Random Trees * (2011)

Same node selection process

1. chose random node in state space, find nearest neighbor in node graph 
2. if no obscatle, place new node at random or max connection distance 
3. DIFFERENCE is connection
4. instead of nearest node, we check for nodes in search radius of the new node
    find node that maintains tree structure and minimizes path length
5. we can stop adding nodes when we are happy with the result
6. now have optimal paths between any points in the environment
'''