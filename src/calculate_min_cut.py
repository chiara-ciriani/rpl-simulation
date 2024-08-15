import networkx as nx

def extract_edges(nodes):
    edges = []
    for node in nodes:
        for neighbor, quality in node.link_quality.items():
            # Avoid duplicate edges (assuming undirected graph)
            if neighbor in nodes:
                edges.append((node.id, neighbor.id, quality))
    return edges

def calculate_min_cut(nodes):
    edges = extract_edges(nodes)
    
    # Crear un grafo basado en el dominio actual
    G = nx.Graph()
    G.add_nodes_from(node.id for node in nodes)
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2])
    
    # Calcular la conectividad global (vertex y edge cuts)
    min_vertex_cut = nx.node_connectivity(G)
    min_edge_cut = nx.edge_connectivity(G)

    return min_vertex_cut, min_edge_cut
