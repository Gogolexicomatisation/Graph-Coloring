import math
from graph import Graph
from step2 import adjacent_list

# Models the antenna frequency problem using an adjacency list and a specified number of vertices, 
# which are then input to the graph coloring function in step 2.
def model_antenna_frequency(antenna_list):
    adj_list = []
    vertices = len(antenna_list)
    for i in range(vertices):
        for j in range(vertices):
            if  j <= i:
                continue
            # Add the link to the adjacency list if the distance is inferior to 8.7 km
            if math.sqrt((antenna_list[j][0] - antenna_list[i][0])**2 + (antenna_list[j][1] - antenna_list[i][1])**2) < 8.7:
                adj_list.append((i+1, j+1))
    return adj_list, vertices



#Example

antenna_1 = (0, 0)
antenna_2 = (3, 5.2)
antenna_3 = (6, 0)
antenna_4 = (9, -5.2)
antenna_5 = (9, 0)
antenna_6 = (9, 5.2)
antenna_7 = (9, 10.4)
antenna_8 = (12, 0)

antennas = [antenna_1, antenna_2, antenna_3, antenna_4, antenna_5, antenna_6, antenna_7, antenna_8]

adjacent_list = model_antenna_frequency(antennas)[0]

graph = Graph(len(antennas))
graph.add_adjacency_list(adjacent_list)
graph.visualize()