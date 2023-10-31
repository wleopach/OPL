import pickle
tree = pickle.load(open('Data/Grafo_rutas0_Augusta_2023-10-27T13_00_00.000Z (1).pickle', 'rb'))


nodes = list(tree.nodes)
node_enum = {nodes[i]: i for i in range(len(nodes))}
edges = list(tree.edges)
edges_ = [f"{{ source: 'Node {node_enum[edges[i][0]]}', target: 'Node {node_enum[edges[i][1]]}' }}" for i in range(len(edges))]


color_map = {'0': 'yellow', '1': 'green', '2': 'red', '3': 'blue'}
colors = [color_map[node.split('#')[0]] for node in nodes ]
nodes_ = [f"{{ id: 'Node {i}', color: '{colors[i]}' }}" for i in range(len(nodes))]
