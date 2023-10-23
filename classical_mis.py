def int_to_binary(n, size=0):
    if n == 0:
        return '0'.rjust(size, '0')
    
    binary = ''
    while n > 0:
        binary = str(n % 2) + binary
        n = n // 2
        
    return binary.rjust(size, '0')


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
    
    
def combinatorial_optimization_MIS(adj_list, vertices):
    cost_list = []
    for i in range(2**vertices):
        number = int_to_binary(i, vertices)
        cost_list.append(cost_function(number, vertices, adj_list))
    return int_to_binary(cost_list.index(min(cost_list)), vertices)

# def graph_coloring(adj_list, vertices):


# adjacent_list = [(1,2), (2,3)]
# vert = 3

# adjacent_list = [(1,2), (2,3), (2,4), (3,4), (1, 3)]
# vert = 4

adjacent_list = [(1,2), (2,3), (2,4), (4,5), (4,6), (5,6), (4,7), (7,8), (7,9), (7,10), (8,9)]
vert = 10

print(combinatorial_optimization_MIS(adjacent_list, vert))

        
        


        
