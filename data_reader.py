import pandas as pd
import heapq
from math import radians, sin, cos, sqrt, atan2


def haversine(coords1, coords2):
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(coords1[0])
    lon1 = radians(coords1[1])
    lat2 = radians(coords2[0])
    lon2 = radians(coords2[1])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius_of_earth = 3958.8  # Radius of Earth in miles
    distance = radius_of_earth * c

    return distance


def adjacent(i, j):
    pickup_upper_bound = extracted_df.loc[nodes[i]]['pickupEnd']
    end_next_pick_up = extracted_df.loc[nodes[j]]['pickupEnd']
    if pickup_upper_bound > end_next_pick_up:
        return 0
    connection = haversine(extracted_df.loc[nodes[i]]['destination_coords'],
                           extracted_df.loc[nodes[i]]['origin_coords']) / 60
    connection = pd.Timedelta(hours=int(connection) + 3)
    result = (pickup_upper_bound + connection < end_next_pick_up) * 1
    return result


def dijkstra(graph, start):
    # Initialize distances and parents
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    parents = {node: None for node in graph}

    # Create a priority queue and add the start node with distance 0
    priority_queue = [(0, start)]

    while priority_queue:
        # Pop the node with the smallest distance
        current_distance, current_node = heapq.heappop(priority_queue)

        # Update distances of neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parents[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, parents


def shortest_path(graph, start, end):
    distances, parents = dijkstra(graph, start)

    # Reconstruct path from end to start
    path = []
    current_node = end
    while current_node is not None:
        path.insert(0, current_node)
        current_node = parents[current_node]

    return path, distances[end]

data = pd.read_csv('Data/datdf0.csv')
data['origin'] = data['origin'].apply(eval)
data['destination'] = data['destination'].apply(eval)

trips = [(row[1]['matchId'], row[1]['origin']['city'], row[1]['origin']['city'], row[1]['tripMiles'] / 60,
          row[1]['pickupDate'], row[1]['endDate'], row[1]['rate'],
          (row[1]['origin']['latitude'], row[1]['origin']['longitude']),
          (row[1]['destination']['latitude'], row[1]['destination']['longitude'])
          ) for row in data.iterrows()]

columns = ['matchId', 'origin', 'destiny', 'tripHours', 'pickupStart', 'pickupEnd',
           'rate', 'origin_coords', 'destination_coords']
extracted_df = pd.DataFrame(trips, columns=columns)
extracted_df.drop_duplicates(inplace=True)

extracted_df['pickupStart'] = pd.to_datetime(extracted_df['pickupStart'])
extracted_df['pickupEnd'] = pd.to_datetime(extracted_df['pickupEnd'])
# Group by 'matchId' and find the index of the row with the latest 'pickupDate'
latest_indices = extracted_df.groupby('matchId')['pickupStart'].idxmax()
extracted_df = extracted_df.loc[latest_indices]

extracted_df.set_index('matchId', inplace=True)
nodes = extracted_df.index
edges = {(i, j) for i in range(len(nodes)) for j in range(len(nodes)) if adjacent(i, j) == 1}
cost = {ed: extracted_df.loc[nodes[ed[1]]]['rate'] for ed in edges}
graph = {i: {edge[1]: cost[edge] for edge in edges if edge[0] == i} for i in range(len(nodes))}

start_node = 0
end_node = 198

path, distance = shortest_path(graph, start_node, end_node)
print(f"Shortest path from {start_node} to {end_node}: {path}")
print(f"Distance: {distance}")