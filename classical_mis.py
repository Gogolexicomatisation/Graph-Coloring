# adjacent_list = [(1,2), (2,3)]
# vert = 3

adjacent_list = [(1,2), (2,3), (2,4), (3,4)]
vert = 4

def find_MIS(adj_list, vertices):
    unlinked = []
    for i in range(1, vertices + 1):
        for j in range(1, vertices + 1):
            if i==j:
                continue
            if ((i, j) not in adj_list and (j, i) not in adj_list) and (j, i) not in unlinked:
                unlinked.append((i,j))
    return unlinked

print(find_MIS(adjacent_list, vert))

# - somme xi + 2 * somme xi*xj

def int_to_binary(n, size=0):
    if n == 0:
        return '0'.rjust(size, '0')
    
    binary = ''
    while n > 0:
        binary = str(n % 2) + binary
        n = n // 2
        
    return binary.rjust(size, '0')



def combinatorial_optimization_MIS(adj_list, vertices):
    cost_list = []
    for i in range(2**vertices):
        number = int_to_binary(i)
        


        
        


        
