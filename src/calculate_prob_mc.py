import random
import networkx as nx

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

def is_connected(G, source_id, destination_id):
    return nx.has_path(G, source=source_id, target=destination_id)

def monte_carlo_simulation(nodes, source_id, destination_id, num_simulations):
    edges = extract_edges(nodes)
    success_count = 0
    
    for _ in range(num_simulations):
        G = generate_random_graph(nodes, edges)
        if is_connected(G, source_id, destination_id):
            success_count += 1
    
    return success_count / num_simulations
