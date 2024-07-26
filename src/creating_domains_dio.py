import math
import random
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

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

def compute_tracks_multipath(nodes, verbose):
    # Compute shortest paths using Dijkstra's algorithm and create tracks
    graph = nx.Graph()
    for node in nodes:
        for neighbor in node.neighbors:
            link_quality = node.link_quality[neighbor]
            weight = 1 - link_quality  # Weight is 1 - PDR
            graph.add_edge(node.id, neighbor.id, weight=weight)

    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    track_nodes = set()

    for street_light in street_lights:
        targets = [sl.id for sl in street_lights if sl.id != street_light.id]
        track = Track(street_light.id, targets)
        
        for target in targets:
            if street_light.id in graph and target in graph:
                try:
                    # First shortest path
                    path1 = nx.shortest_path(graph, source=street_light.id, target=target, weight='weight')
                    
                    route_nodes1 = [nodes[node_id] for node_id in path1]
                    track_nodes.update(route_nodes1)
                    track.install_route_to_target(target, route_nodes1)

                    # Remove edges in the first path
                    graph_removed_edges = graph.copy()
                    path_edges = [(path1[i], path1[i+1]) for i in range(len(path1)-1)]
                    graph_removed_edges.remove_edges_from(path_edges)
                    
                    # Second shortest path
                    path2 = nx.shortest_path(graph_removed_edges, source=street_light.id, target=target, weight='weight')
                    
                    route_nodes2 = [nodes[node_id] for node_id in path2]
                    track_nodes.update(route_nodes2)
                    track.install_route_to_target(target, route_nodes2)
                except nx.NetworkXNoPath:
                    if verbose: 
                        print(f"No disjoint paths found between {street_light.id} and {target}")
            else:
                if verbose:
                    print(f"Either source {street_light.id} or target {target} is not in the graph")
        
        street_light.install_track(track, verbose)
    
    return track_nodes

def compute_tracks_multipath_disjoint_paths(nodes, verbose):
    # Compute shortest paths using Dijkstra's algorithm and create tracks
    graph = nx.Graph()
    for node in nodes:
        for neighbor in node.neighbors:
            link_quality = node.link_quality[neighbor]
            weight = 1 - link_quality  # Weight is 1 - PDR
            graph.add_edge(node.id, neighbor.id, weight=weight)

    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    track_nodes = set()

    for street_light in street_lights:
        targets = [sl.id for sl in street_lights if sl.id != street_light.id]
        track = Track(street_light.id, targets)
        
        for target in targets:
            if street_light.id in graph and target in graph:
                try:
                    # First shortest path
                    path1 = nx.shortest_path(graph, source=street_light.id, target=target, weight='weight')
                    
                    route_nodes1 = [nodes[node_id] for node_id in path1]
                    track_nodes.update(route_nodes1)
                    track.install_route_to_target(target, route_nodes1)

                    # Remove edges in the first path
                    graph_removed_nodes = graph.copy()
                    
                    for node in path1:
                        if node != street_light.id and node != target:
                            graph_removed_nodes.remove_node(node)

                    if len(path1) == 2:
                        # Remove edges in the first path
                        path_edges = [(path1[i], path1[i+1]) for i in range(len(path1)-1)]
                        graph_removed_nodes.remove_edges_from(path_edges)
                    
                    # Second shortest path
                    path2 = nx.shortest_path(graph_removed_nodes, source=street_light.id, target=target, weight='weight')
                    
                    route_nodes2 = [nodes[node_id] for node_id in path2] 
                    track_nodes.update(route_nodes2)
                    track.install_route_to_target(target, route_nodes2)
                except nx.NetworkXNoPath:
                    if verbose: 
                        print(f"No disjoint paths found between {street_light.id} and {target}")
            else:
                if verbose:
                    print(f"Either source {street_light.id} or target {target} is not in the graph")
        
        street_light.install_track(track, verbose)
    
    return track_nodes

def add_nodes_to_multipath_domain(mpl_domain, track_nodes, verbose):
    for node in track_nodes:
        mpl_domain.add_node(node, verbose)

    if verbose:
        print(f"MPL Domain: {mpl_domain}")

def add_nodes_to_multipath_domain_common_neighbors(mpl_domain, nodes, verbose):
    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    # Function to add nodes to MPL domain
    def add_node_to_domain(node):
        if node not in mpl_domain.nodes:
            mpl_domain.add_node(node, verbose)

    # Function to calculate the PDR between two nodes using ETX
    def calculate_pdr(node1, node2):
        etx = node1.calculate_etx(node2)
        if etx > 0:
            return 1 / etx
        return 0

    for i in range(len(street_lights)):
        for j in range(i + 1, len(street_lights)):
            sl1 = street_lights[i]
            sl2 = street_lights[j]

            common_neighbors = set(sl1.neighbors).intersection(sl2.neighbors)
            if common_neighbors:
                best_neighbor = None
                max_pdr_product = 0

                # ELEGIR NEIGHBOR QUE MAXIMICE PDR
                for neighbor in common_neighbors:
                    pdr_sl1_to_neighbor = calculate_pdr(sl1, neighbor)
                    pdr_neighbor_to_sl2 = calculate_pdr(neighbor, sl2)
                    pdr_product = pdr_sl1_to_neighbor * pdr_neighbor_to_sl2

                    if pdr_product > max_pdr_product:
                        max_pdr_product = pdr_product
                        best_neighbor = neighbor

                if best_neighbor:
                    add_node_to_domain(best_neighbor)
                    add_node_to_domain(sl1)
                    add_node_to_domain(sl2)
                    if verbose:
                        print(f"Added {best_neighbor.get_id()} as common neighbor of {sl1.get_id()} and {sl2.get_id()}")

    if verbose:
        print(f"MPL Domain: {mpl_domain}")

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

# Función para agregar street lights al dominio MPL
def add_nodes_to_minimal_domain(mpl_domain, nodes, verbose):
    street_lights = [node for node in nodes if isinstance(node, StreetLight)]
    
    for street_light in street_lights:
        mpl_domain.add_node(street_light, verbose)

    if verbose:
        print(f"MPL Domain: {mpl_domain}")

def create_network_with_dio(env, width, height, num_nodes, num_street_lights, tx_range, max_distance, verbose):
    # Inicializar el terreno y las posiciones de los nodos
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

    for node in nodes:
        for other_node in nodes:
            if node != other_node:
                dist = math.sqrt((node.x - other_node.x) ** 2 + (node.y - other_node.y) ** 2)
                if dist <= tx_range:
                    link_quality = random.uniform(0.5, 0.95)  # Random link quality between 0.5 and 0.95
                    node.add_neighbor(other_node, link_quality)
                    other_node.add_neighbor(node, link_quality) 

    # Randomly select a root node that is not a street light
    root_node_idx = random.choice([node.id for node in nodes if not isinstance(node, StreetLight)])
    root_node = nodes[root_node_idx]
    root_node.set_as_root(verbose, True)

    return nodes, root_node


def plot_network(nodes, mpl_domain_1, mpl_domain_2=None, mpl_domain_3=None):
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
        elif mpl_domain_2 and node in mpl_domain_2.nodes:
            node_colors.append('violet')  # Nodos del dominio MPL en violeta
            node_sizes.append(400)
        elif mpl_domain_3 and node in mpl_domain_3.nodes:
            node_colors.append('yellow')  # Nodos del dominio MPL en violeta
            node_sizes.append(400)
        else:
            node_colors.append('skyblue')  # Otros nodos en azul
            node_sizes.append(300)

    plt.figure(figsize=(12, 12))
    G = nx.DiGraph()

    for node in nodes:
        G.add_node(node.id, pos=(node.x, node.y))

    for node in nodes:
        if node.preferred_parent:
            G.add_edge(node.preferred_parent.id, node.id)
    
    # Add neighbor links with link quality as color intensity and annotate with link quality numbers
    for node in nodes:
        for neighbor in node.neighbors:
            if not G.has_edge(node.id, neighbor.id):
                link_quality = node.get_link_quality(neighbor)
                intensity = 1 - link_quality  # Higher quality means darker color
                plt.plot([node.x, neighbor.x], [node.y, neighbor.y], color=(1, 0, 0, intensity), linestyle='--', alpha=0.5)
                mid_x = (node.x + neighbor.x) / 2
                mid_y = (node.y + neighbor.y) / 2
                plt.text(mid_x, mid_y, f'{link_quality:.2f}', fontsize=9, ha='center', va='center', color='black')
    
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=10, font_weight='bold')

    plt.title("Network Topology with DODAG and Link Quality")
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Create custom legend
    legend_elements = [
        Patch(facecolor='red', edgecolor='black', label='DODAG Root'),
        Patch(facecolor='skyblue', edgecolor='black', label='Nodes'),
        Patch(facecolor='green', edgecolor='black', label='Street Light'),
    ]

    if mpl_domain_2:
        legend_elements.append(Patch(facecolor='orange', edgecolor='black', label='Domain Removed Edges'))
        legend_elements.append(Patch(facecolor='violet', edgecolor='black', label='Common Neighbor Domain'))
        legend_elements.append(Patch(facecolor='yellow', edgecolor='black', label='Domain Disjoint Paths'))
    else:
        legend_elements.append(Patch(facecolor='orange', edgecolor='black', label='Minimal Domain'))

    plt.legend(handles=legend_elements, loc='upper right', title='Node Types')

    plt.show()

