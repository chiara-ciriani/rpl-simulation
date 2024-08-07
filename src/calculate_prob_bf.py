import itertools
import networkx as nx

def generate_all_configurations(edges):
    # Generar todas las configuraciones posibles de enlaces activos/inactivos
    return list(itertools.product([0, 1], repeat=len(edges)))

def configuration_to_graph(config, edges, nodes):
    # Crear un grafo basado en una configuración dada
    G = nx.Graph()
    G.add_nodes_from(node.id for node in nodes)
    for edge, active in zip(edges, config):
        if active == 1:
            G.add_edge(edge[0], edge[1], weight=edge[2])
    return G

def calculate_configuration_probability(config, edges, link_probabilities):
    # Calcular la probabilidad de una configuración dada
    probability = 1.0
    for edge, active in zip(edges, config):
        if active == 1:
            probability *= link_probabilities[(edge[0], edge[1])]
        else:
            probability *= (1 - link_probabilities[(edge[0], edge[1])])
    return probability

def brute_force_solution(nodes, source_id, destination_id):
    # Crear lista de enlaces y probabilidades de enlace
    edges = []
    link_probabilities = {}
    
    for node in nodes:
        for neighbor in node.neighbors:
            edges.append((node.id, neighbor.id, node.link_quality[neighbor.id]))
            link_probabilities[(node.id, neighbor.id)] = node.link_quality[neighbor.id]

    all_configurations = generate_all_configurations(edges)
    total_probability = 0.0
    
    for config in all_configurations:
        G = configuration_to_graph(config, edges, nodes)
        if nx.has_path(G, source=source_id, target=destination_id):
            config_prob = calculate_configuration_probability(config, edges, link_probabilities)
            total_probability += config_prob
    
    return total_probability

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

# Calcular la probabilidad por fuerza bruta
probability = brute_force_solution(nodes, source_id, destination_id)
# print(f'Brute Force Probability: {probability}')
