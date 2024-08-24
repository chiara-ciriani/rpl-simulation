import random
import networkx as nx

AVG_TRANSMISSION_TIME = 365.8

def extract_edges(nodes):
    edges = []
    for node in nodes:
        for neighbor, quality in node.link_quality.items():
            # Avoid duplicate edges (assuming undirected graph)
            if node.id < neighbor.id:
                edges.append((node.id, neighbor.id, quality))
    return edges

def generate_random_graph(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(node.id for node in nodes)
    for edge in edges:
        if random.random() <= edge[2]:
            G.add_edge(edge[0], edge[1])
    return G

def is_connected_to_all(G, source_id, destination_ids):
    # Check if the source is connected to all destination_ids
    return all(nx.has_path(G, source=source_id, target=dest_id) for dest_id in destination_ids)

def calculate_longest_shortest_path_time(G, source_id, destination_ids):
    # Calculate the shortest path length from source to each destination
    shortest_paths = [nx.shortest_path_length(G, source=source_id, target=dest_id) for dest_id in destination_ids]
    
    # Find the longest of these shortest paths
    longest_path_length = max(shortest_paths)
    
    # Calculate the time based on the longest path length and the average transmission time
    return longest_path_length * AVG_TRANSMISSION_TIME

def monte_carlo_simulation(nodes, source_id, destination_ids, num_simulations):
    edges = extract_edges(nodes)
    success_count = 0
    total_time = 0
    
    for _ in range(num_simulations):
        G = generate_random_graph(nodes, edges)
        if is_connected_to_all(G, source_id, destination_ids):
            success_count += 1
            # Calculate time for the message to reach the last street light
            time_for_last_street_light = calculate_longest_shortest_path_time(G, source_id, destination_ids)
            total_time += time_for_last_street_light
    
    success_probability = success_count / num_simulations
    average_time_for_success = total_time / success_count if success_count > 0 else 0
    
    return success_probability, average_time_for_success