import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

def draw_graph(arrangement_tuple):
    G = nx.Graph()

    for node, _ in arrangement_tuple:
        G.add_node(node)

    for i in range(len(arrangement_tuple)-1):
        G.add_edge(arrangement_tuple[i][0], arrangement_tuple[i+1][0])

    for _, position in arrangement_tuple:
        Counter()

    values = [-1, 0, 1]
    counts = [sum(tuple_index.count(val) for tuple_index in sorted_arrangement) for val in values]


    node_positions = []
    current_value = 0

    for count in counts:
        increment = 2.0 / (2* count)
        for _ in range(count):
            node_positions.append(current_value)
            current_value += increment    

            
    pos = {utensil: (i, 0) for ((utensil, _), i) in zip(arrangement_tuple, node_positions)}


    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', font_size=10, font_color='black', font_weight='bold', arrowsize=20)

    plt.title("Vertices Graph based on Arrangement Tuple")
    plt.show()

# Example usage
arrangement_dict = {'plate': 'center', 'fork': 'left', 'spoon': 'right', 'knife': 'right'}
index_position = {"center": 0, "left": -1, "right": 1}

arrangement_tuple = [(key, index_position[val]) for key, val in arrangement_dict.items()]

sorted_arrangement = sorted(arrangement_tuple, key=lambda x: x[1])

draw_graph(sorted_arrangement)