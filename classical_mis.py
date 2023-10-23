from math import inf
from utils import int_to_binary, have_common_bit


# calculate the cost of a specific configuration
def cost_function(bit_string, length, adj_list):
    cost = 0
    for i in range(length):
        cost -= int(bit_string[i])
        for j in range(length):
            if i == j:
                continue
            
            if (i+1, j+1) in adj_list:  
                cost += 2 * int(bit_string[i]) * int(bit_string[j])
                
    return cost

# return the cost function and the minimal cost configuration
def combinatorial_optimization_MIS(adj_list, actual_vertices, vertices, colored_edges):
    cost_list = []
    for i in range(2**vertices):
        number = int_to_binary(i, vertices)
        if have_common_bit(number, colored_edges):
            cost_list.append(inf)
            continue
        cost_list.append(cost_function(number, vertices, adj_list))
    return int_to_binary(cost_list.index(min(cost_list)), vertices) #PROBLEMS?

def remove_edges(new_adjacent_list, index):
    return [t for t in new_adjacent_list if index not in t]


def remove_vertices_edges(bit_string, vertices ,adjacent_list):
    new_adj_list = adjacent_list.copy()
    for i in range(len(bit_string)):
        if bit_string[i] == '1':
            new_adj_list = remove_edges(new_adj_list, i+1)
            vertices -= 1
    return new_adj_list, vertices

def count_color(color_list, vertices):    
    colored_edges = '0' * vertices
    for elements in color_list:
        colored_edges = int_to_binary(int(elements, 2) | int(colored_edges, 2), vertices)
    return colored_edges

def graph_coloring(adj_list, vertices):
    
    actual_vertices = vertices
    color_list = []
    colored_edges = count_color(color_list, vertices)
    while adj_list != []:
        mis_bit_string = combinatorial_optimization_MIS(adj_list, actual_vertices, vertices, colored_edges)
        color_list.append(mis_bit_string)
        adj_list, actual_vertices = remove_vertices_edges(mis_bit_string, actual_vertices, adj_list)
        colored_edges = count_color(color_list, vertices)
    
    last_mis_bit_string = combinatorial_optimization_MIS(adj_list, actual_vertices, vertices, colored_edges)
    color_list.append(last_mis_bit_string)
    return color_list


# adjacent_list = [(1,2), (2,3)]
# vert = 3



# adjacent_list = [(1,2), (2,3), (2,4), (3,4), (1, 3)]
# vert = 4





adjacent_list = [(1,2), (2,3), (2,4), (4,5), (4,6), (5,6), (4,7), (7,8), (7,9), (7,10), (8,9)]
vert = 10

print(graph_coloring(adjacent_list, vert))
# print(combinatorial_optimization_MIS(adjacent_list, vert))


