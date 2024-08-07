import math
import random
import networkx as nx
from matplotlib import pyplot as plt

from node import Node
from street_light import StreetLight
from track import Track

def compute_tracks(nodes, verbose):
     # Compute shortest paths using Dijkstra's algorithm and create tracks
    graph = nx.Graph()
    for node in nodes:
        for neighbor in node.neighbors:
            graph.add_edge(node.id, neighbor.id, weight=1)  # Assuming equal weight for all edges

    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    for street_light in street_lights:
        targets = [sl.id for sl in street_lights if sl.id != street_light.id]
        track = Track(street_light.id, targets)
        for target in targets:
            if street_light.id in graph and target in graph:
                path = nx.shortest_path(graph, source=street_light.id, target=target, weight='weight')
                route_nodes = [nodes[node_id] for node_id in path]
                track.install_route_to_target(target, route_nodes)
            else:
                if verbose: print(f"Either source {street_light.id} or target {target} is not in the graph")
        street_light.install_track(track, verbose)

# Función para agregar nodos al dominio MPL
def add_nodes_to_mpl_domain_disjoint_path(mpl_domain, nodes, verbose):
    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    # Función para agregar nodos al dominio MPL
    def add_node_to_domain(node):
        if node not in mpl_domain.nodes:
            mpl_domain.add_node(node, verbose)

    for i in range(len(street_lights)):
        for j in range(i + 1, len(street_lights)):
            sl1 = street_lights[i]
            sl2 = street_lights[j]

            common_neighbors = set(sl1.neighbors).intersection(sl2.neighbors)
            if common_neighbors:
                best_neighbor = None
                best_dist = float('inf')

                for neighbor in common_neighbors:
                    dist1 = math.sqrt((neighbor.x - sl1.x) ** 2 + (neighbor.y - sl1.y) ** 2)
                    dist2 = math.sqrt((neighbor.x - sl2.x) ** 2 + (neighbor.y - sl2.y) ** 2)
                    mid_dist = abs(dist1 - dist2)

                    if mid_dist < best_dist:
                        best_dist = mid_dist
                        best_neighbor = neighbor

                if best_neighbor:
                    add_node_to_domain(best_neighbor)
                    add_node_to_domain(sl1)
                    add_node_to_domain(sl2)
                    if verbose:
                        print(f"Added {best_neighbor.id} as common neighbor of {sl1.id} and {sl2.id}")

    if verbose:
        print(f"MPL Domain: {mpl_domain}")

# Función para agregar nodos al dominio MPL
def add_street_light_to_mpl_domain(mpl_domain, nodes, verbose):
    street_lights = [node for node in nodes if isinstance(node, StreetLight)]
    
    for street_light in street_lights:
        mpl_domain.add_node(street_light, verbose)

    if verbose:
        print(f"MPL Domain: {mpl_domain}")



def create_network_with_spanning_tree(env, num_nodes, num_street_lights, tx_range, max_distance, verbose):
    # Inicializar el terreno y las posiciones de los nodos
    width, height = 100, 100
    nodes = []
    
    # Calcular la posición de las street lights asegurando que la distancia máxima entre ellas sea max_distance
    street_light_positions = []
    x_start = width // 4
    y = height // 2
    for i in range(num_street_lights):
        x = x_start + i * max_distance
        if x > width:
            x = width
        street_light_positions.append((x, y))
    
    for i, pos in enumerate(street_light_positions):
        nodes.append(StreetLight(env, i, pos[0], pos[1], tx_range))

    for i in range(num_street_lights, num_nodes + num_street_lights):
        x, y = random.uniform(0, width), random.uniform(0, height)
        nodes.append(Node(env, i, x, y, tx_range, verbose))

    # Crear un grafo completo y asignar pesos basados en la distancia
    G = nx.Graph()
    for node in nodes:
        G.add_node(node.id, pos=(node.x, node.y))

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            dist = math.sqrt((nodes[i].x - nodes[j].x) ** 2 + (nodes[i].y - nodes[j].y) ** 2)
            if dist <= tx_range:
                G.add_edge(nodes[i].id, nodes[j].id, weight=dist)

    # Crear el MST
    T = nx.minimum_spanning_tree(G, weight='weight')

    # Asignar vecinos basados en el MST
    for u, v in T.edges():
        nodes[u].neighbors.append(nodes[v])
        nodes[v].neighbors.append(nodes[u])

    # Asignar vecinos basados en el rango de transmisión
    for node in nodes:
        for other_node in nodes:
            if node != other_node:
                dist = math.sqrt((node.x - other_node.x) ** 2 + (node.y - other_node.y) ** 2)
                if dist <= tx_range and other_node not in node.neighbors:
                    node.neighbors.append(other_node)

    # Randomly select a root node that is not a street light
    root_node_idx = random.choice([node.id for node in nodes if not isinstance(node, StreetLight)])
    root_node = nodes[root_node_idx]
    root_node.set_as_root(verbose)

    # Assign preferred parents based on the MST structure
    parent_map = nx.predecessor(T, root_node_idx)
    for node in nodes:
        if not node.is_root:
            if node.id in parent_map and parent_map[node.id]:
                parent_id = parent_map[node.id][0]
                parent_node = nodes[parent_id]
                node.preferred_parent = parent_node
                parent_node.children.append(node)
            else:
                # Si el nodo no tiene un parent en el parent_map, asignar un parent alternativo basado en la distancia
                closest_parent = None
                min_dist = float('inf')
                for neighbor in node.neighbors:
                    if neighbor.rank is not None:
                        dist = math.sqrt((node.x - neighbor.x) ** 2 + (node.y - neighbor.y) ** 2)
                        if dist < min_dist:
                            min_dist = dist
                            closest_parent = neighbor
                if closest_parent:
                    node.preferred_parent = closest_parent
                    closest_parent.children.append(node)

    return nodes, T, root_node


def plot_network(nodes, T, mpl_domain_1, mpl_domain_2):
    pos = {node.id: (node.x, node.y) for node in nodes}
    labels = {node.id: node.id for node in nodes}

    node_colors = []
    node_sizes = []

    for node in nodes:
        if node.is_dodag_root():
            node_colors.append('red')  # Raíz en rojo
            node_sizes.append(700)
        elif isinstance(node, StreetLight):
            node_colors.append('green')  # Street lights en verde
            node_sizes.append(500)
        elif node in mpl_domain_1.nodes:
            node_colors.append('orange')  # Nodos del dominio MPL en naranja
            node_sizes.append(400)
        elif node in mpl_domain_2.nodes:
            node_colors.append('violet')  # Nodos del dominio MPL en violeta
            node_sizes.append(400)
        else:
            node_colors.append('skyblue')  # Otros nodos en azul
            node_sizes.append(300)

    plt.figure(figsize=(12, 12))
    nx.draw(T, pos, labels=labels, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=10, font_weight='bold')
    nx.draw_networkx_edge_labels(T, pos, edge_labels={(u, v): f"{d['weight']:.1f}" for u, v, d in T.edges(data=True)})

    # Dibujar enlaces de vecinos basados en el rango de transmisión en color diferente
    for node in nodes:
        for neighbor in node.neighbors:
            if not T.has_edge(node.id, neighbor.id):
                plt.plot([node.x, neighbor.x], [node.y, neighbor.y], 'c--', alpha=0.5)  # Enlaces de vecinos en cian discontinuo

    plt.title("Network Topology with Spanning Tree, Neighbor Links, and MPL Domain")
    plt.show()
