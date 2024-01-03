#pip install networkx matplotlib


import networkx as nx
import matplotlib.pyplot as plt

# Given tuple with objects and directions
arrangement_tuple = (('plate', 'center'), ('fork', 'right'), ('spoon', 'left'))

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges based on the arrangement tuple
for obj, direction in arrangement_tuple:
    G.add_node(obj)  # Add the object as a node
    G.add_edge(obj, direction)  # Add an edge from the object to the direction

# Plot the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1000, node_color='skyblue', font_size=10, edge_color='gray')
plt.show()
