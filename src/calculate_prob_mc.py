import random
import networkx as nx

def extract_edges(nodes):
    edges = []
    for node in nodes:
        for neighbor in node.neighbors:
            edges.append((node.id, neighbor.id, node.get_link_quality(neighbor)))
    return edges

def generate_random_graph(nodes, edges):
    G = nx.Graph()
    G.add_nodes_from(node.id for node in nodes)
    for edge in edges:
        if random.random() <= edge[2]:
            G.add_edge(edge[0], edge[1], weight=edge[2])
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

# Ejemplo de uso
class Node:
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.link_quality = {}

    def add_neighbor(self, neighbor, link_quality):
        self.neighbors.append(neighbor)
        self.link_quality[neighbor.id] = link_quality

    def get_link_quality(self, neighbor):
        return self.link_quality.get(neighbor.id, 1.0)

# Crear nodos y enlaces
nodes = [Node(i) for i in range(1, 5)]
nodes[0].add_neighbor(nodes[1], 0.9)
nodes[1].add_neighbor(nodes[0], 0.9)
nodes[1].add_neighbor(nodes[2], 0.8)
nodes[2].add_neighbor(nodes[1], 0.8)
nodes[2].add_neighbor(nodes[3], 0.7)
nodes[3].add_neighbor(nodes[2], 0.7)

# Definir el origen y destino
source_id = 1
destination_id = 4

# Número de simulaciones
num_simulations = 10000

# Ejecutar la simulación de Monte Carlo
probability = monte_carlo_simulation(nodes, source_id, destination_id, num_simulations)
# print(f'Monte Carlo Probability: {probability}')
