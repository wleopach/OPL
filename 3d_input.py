import pickle
import json
import csv

tree = pickle.load(open('Data/Grafo_rutas0_Augusta_2023-10-27T13_00_00.000Z (1).pickle', 'rb'))

nodes = list(tree.nodes)
node_enum = {nodes[i]: i for i in range(len(nodes))}
edges = list(tree.edges)
edges_ = [{"source": f"Node {node_enum[edges[i][0]]}",
           "target": f"Node {node_enum[edges[i][1]]}"} for i in range(len(edges))]

edges_ = edges_[:100]
color_map = {'0': 'yellow', '1': 'green', '2': 'red', '3': 'blue'}
colors = [color_map[node.split('#')[0]] for node in nodes]
nodes_ = [{"id": f"Node {i}", "color": f"{colors[i]}", "city": f"{nodes[i].split('#')[2]}"} for i in range(len(nodes))]

data = {"edges": edges_, "nodes": nodes_}

# Define the file path where you want to save the JSON file
file_path = "Data/graph_data.json"

# Write the data to a JSON file
with open(file_path, "w") as json_file:
    json.dump(data, json_file)


def find_paths(graph):
    def dfs(node, path):
        if node not in visited:
            visited.add(node)
            path.append(node)
            paths.append("/".join(path))
            for edge in graph:
                if edge["source"] == node:
                    dfs(edge["target"], path)
            visited.remove(node)
            path.pop()

    visited = set()
    paths = []
    for edge in graph:
        dfs(edge["source"], [])

    return paths


def save_paths_to_csv(paths, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["size", "path"])
        for path in paths:
            writer.writerow(["", path])


paths = find_paths(edges_)
filename = "Data/dep.csv"
save_paths_to_csv(paths, filename)
