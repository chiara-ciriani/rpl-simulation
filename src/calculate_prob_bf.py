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
            G.add_edge(edge[0], edge[1])
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
        for neighbor, quality in node.link_quality.items():
            if (node.id, neighbor.id) not in link_probabilities and (neighbor.id, node.id) not in link_probabilities:
                edges.append((node.id, neighbor.id))
                link_probabilities[(node.id, neighbor.id)] = quality

    all_configurations = generate_all_configurations(edges)
    total_probability = 0.0
    
    for config in all_configurations:
        G = configuration_to_graph(config, edges, nodes)
        if nx.has_path(G, source=source_id, target=destination_id):
            config_prob = calculate_configuration_probability(config, edges, link_probabilities)
            total_probability += config_prob
    
    return total_probability
