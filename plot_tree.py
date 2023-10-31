import matplotlib.pyplot as plt
import networkx as nx
import pickle
tree = pickle.load(open('Data/Grafo_rutas0.pickle', 'rb'))



def custom_layout(tree, root):
    pos = {root: (0, 0)}
    level = {root: 0}

    def dfs(node, parent):
        children = list(tree.neighbors(node))
        num_children = len(children)
        if num_children == 0:
            return
        level_y = level[parent] - 1
        for i, child in enumerate(children):
            pos[child] = (i - (num_children - 1) / 2, level_y)
            level[child] = level_y
            dfs(child, child)

    dfs(root, root)
    return pos


# Create a sample tree structure


# Define the root node
#root = '0#Louisville#2023-10-04 22:00:00+00:00'
root = '0#Augusta#2023-10-20T13:00:00+00:00'

# Draw the tree with custom layout
pos = custom_layout(tree, root)

repair = {}
# Check if a node exists in pos before updating it
for node in tree.nodes:
    if node not in pos:
        repair[node] = (-1, -2)

pos.update(repair)

# Set the figure size
plt.figure(figsize=(40, 20))  # Adjust the width and height as needed

# Draw nodes

# Define a function to assign colors based on levels
color_map = {0: 'yellow', -1: 'green', -2: 'red', -3: 'blue', -4: 'black', -5: 'orange'}
colors = [color_map[pos[node][1]] for node in tree.nodes ]
nx.draw_networkx_nodes(tree, pos, node_size=1500, node_color= colors)

# Draw edges
nx.draw_networkx_edges(tree, pos, edge_color='gray')

# Draw labels (optional)
labels = {n: n for n in tree.nodes}
nx.draw_networkx_labels(tree, pos, labels, font_size=3, font_color='black')

# Show the plot
plt.axis('off')
plt.show()
nx.write_weighted_edgelist(tree, "weighted_test_edgelist.txt")
nodes = list(tree.nodes)
nodes_ = [f"{{ id: 'Node {i}', color: '{colors[i]}' }}" for i in range(len(nodes))]
node_enum = {nodes[i]: i for i in range(len(nodes))}
edges = list(tree.edges)
edges_ = [f"{{ source: 'Node {node_enum[edges[i][0]]}', target: 'Node {node_enum[edges[i][1]]}' }}" for i in range(len(edges))]