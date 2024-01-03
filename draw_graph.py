import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(arrangement_tuple):
    G = nx.Graph()

    for node, position in arrangement_tuple:
        G.add_node(node)

    for i in range(len(arrangement_tuple)-1):
        G.add_edge(arrangement_tuple[i][0], arrangement_tuple[i+1][0])

    pos = {node: (i, arrangement_tuple.index((node, position))) for i, (node, position) in enumerate(arrangement_tuple)}

    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', font_size=10, font_color='black', font_weight='bold', arrowsize=20)

    plt.title("Vertices Graph based on Arrangement Tuple")
    plt.show()

# Example usage
arrangement_tuple = (('plate', 'center'), ('fork', 'left'), ('spoon', 'right'))
draw_graph(arrangement_tuple)