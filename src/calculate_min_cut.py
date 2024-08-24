import networkx as nx
import matplotlib.pyplot as plt

def extract_edges(nodes):
    edges = []
    for node in nodes:
        for neighbor, quality in node.link_quality.items():
            # Avoid duplicate edges (assuming undirected graph)
            if neighbor in nodes:
                edges.append((node.id, neighbor.id, quality))
    return edges

def plot_graph(G):
    # Dibujar el grafo con posiciones definidas por el algoritmo de layout de NetworkX
    pos = nx.spring_layout(G)  # Puedes cambiar el layout a tu preferencia, e.g., nx.circular_layout(G)
    
    # Dibujar los nodos y las aristas
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=15)
    
    # Dibujar las etiquetas de peso en las aristas
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    # Mostrar el gráfico
    plt.show()

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

    # plot_graph(G)

    return min_vertex_cut, min_edge_cut
