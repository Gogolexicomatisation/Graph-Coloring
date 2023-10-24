import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, num_nodes):
        self.adjacency_list = {i: [] for i in range(1, num_nodes + 1)}
        self.colors = {}

    def add_edge(self, node1, node2):
        if node2 not in self.adjacency_list[node1]:
            self.adjacency_list[node1].append(node2)
        if node1 not in self.adjacency_list[node2]:
            self.adjacency_list[node2].append(node1)

    def add_adjacency_list(self, adj_list):
        for node1, node2 in adj_list:
            self.add_edge(node1, node2)
    
    def color_graph(self, bit_strings):
        color_palette = ['red', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'lime', 'pink', 'teal', 'lavender', 'brown', 'beige', 'gray']
        for idx, bit_string in enumerate(bit_strings):
            for i, bit in enumerate(bit_string):
                if bit == '1':
                    self.colors[i+1] = color_palette[idx]


    def visualize(self):
        G = nx.Graph()
        for node, neighbors in self.adjacency_list.items():
            G.add_node(node)
            for neighbor in neighbors:
                G.add_edge(node, neighbor)

        node_colors = [self.colors.get(node, 'blue') for node in G.nodes()]
        nx.draw(G, with_labels=True, node_size=2000, node_color=node_colors, font_size=20, width=2, edge_color="gray")
        plt.show()