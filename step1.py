import math
from graph import Graph

# Models the antenna frequency problem using an adjacency list and a specified number of vertices, 
# which are then input to the graph coloring function in step 2.
def model_antenna_frequency(antenna_list, block_dist):
    adj_list = []
    vertices = len(antenna_list)
    for i in range(vertices):
        for j in range(vertices):
            if  j <= i:
                continue
            # Add the link to the adjacency list if the distance is inferior to 8.7 km
            if math.sqrt((antenna_list[j][0] - antenna_list[i][0])**2 + (antenna_list[j][1] - antenna_list[i][1])**2) <= block_dist:
                adj_list.append((i+1, j+1))
    return adj_list, vertices  