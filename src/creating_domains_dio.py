import math
import random
import networkx as nx
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

from classes.node import Node
from classes.street_light import StreetLight
from classes.track import Track

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
        street_light.install_track(track, True, verbose)

def compute_tracks_multipath(nodes, verbose):
    # Compute shortest paths using Dijkstra's algorithm and create tracks
    graph = nx.Graph()
    for node in nodes:
        for neighbor in node.neighbors:
            link_quality = node.link_quality[neighbor]
            weight = 1 / link_quality
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
                    try:
                        path2 = nx.shortest_path(graph_removed_edges, source=street_light.id, target=target, weight='weight')
                    except nx.NetworkXNoPath:
                        if verbose:
                            print(f"No disjoint path found between {street_light.id} and {target}. Using the first path again.")
                        path2 = path1  # Use the first path if no disjoint path found
                    
                    route_nodes2 = [nodes[node_id] for node_id in path2]
                    track_nodes.update(route_nodes2)
                    track.install_route_to_target(target, route_nodes2)
                except nx.NetworkXNoPath:
                    if verbose: 
                        print(f"No disjoint paths found between {street_light.id} and {target}")
            else:
                if verbose:
                    print(f"Either source {street_light.id} or target {target} is not in the graph")
        
        street_light.install_track(track, True, verbose)
    
    return track_nodes

def compute_tracks_multipath_disjoint_paths(nodes, verbose):
    # Compute shortest paths using Dijkstra's algorithm and create tracks
    graph = nx.Graph()
    for node in nodes:
        for neighbor in node.neighbors:
            link_quality = node.link_quality[neighbor]
            weight = 1 / link_quality
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
                    try:
                        path2 = nx.shortest_path(graph_removed_nodes, source=street_light.id, target=target, weight='weight')
                    except nx.NetworkXNoPath:
                        if verbose:
                            print(f"No disjoint path found between {street_light.id} and {target}. Using the first path again.")
                        path2 = path1  # Use the first path if no disjoint path found
                    
                    route_nodes2 = [nodes[node_id] for node_id in path2]
                    track_nodes.update(route_nodes2)
                    track.install_route_to_target(target, route_nodes2)

                except nx.NetworkXNoPath:
                    if verbose: 
                        print(f"No disjoint paths found between {street_light.id} and {target}")
            else:
                if verbose:
                    print(f"Either source {street_light.id} or target {target} is not in the graph")
        
        street_light.install_track(track, False, verbose)
    
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

    # Function to calculate the PDR between two nodes
    def calculate_pdr(node1, node2):
        return node1.link_quality[node2]

    for i in range(len(street_lights)):
        # if i + 2 > len(street_lights):
        #     continue
        # for j in range(i + 1, i + 2):
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

def calculate_node_density(width, height, num_nodes):
    area = width * height
    node_density = num_nodes / area
    return node_density

def create_network_with_dio(env, width, height, num_nodes, num_street_lights, tx_range, max_distance, verbose):
    # Initialize the terrain and node positions
    nodes = []
    
    # Calculate total length needed for all street lights with max_distance between them
    total_street_light_length = (num_street_lights - 1) * max_distance
    
    # Calculate starting x position to center street lights
    x_start = (width - total_street_light_length) / 2
    y = height / 2  # Center y position

    street_light_positions = []
    
    # Position the street lights centered in the terrain width
    for i in range(num_street_lights):
        x = x_start + i * max_distance
        street_light_positions.append((x, y))
    
    # Create StreetLight nodes at calculated positions
    for i, pos in enumerate(street_light_positions):
        nodes.append(StreetLight(env, i, pos[0], pos[1], tx_range))

    # Create additional random nodes within the terrain
    for i in range(num_street_lights, num_nodes + num_street_lights):
        x, y = random.uniform(0, width), random.uniform(0, height)
        nodes.append(Node(env, i, x, y, tx_range, verbose))

    # Connect nodes that are within transmission range
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


def plot_network(nodes, mpl_domain_1, mpl_domain_2=None, mpl_domain_3=None, mpl_domain_4=None):
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
            node_colors.append('yellow')  # Nodos del dominio MPL en amarillo
            node_sizes.append(400)
        elif mpl_domain_4 and node in mpl_domain_4.nodes:
            node_colors.append('cyan')  # Nodos del dominio MPL en cyan
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

def plot_domain_dodag(nodes, domain, domain_index, verbose=False):
    """
    Function to plot the DODAG for a specific MPL domain, highlighting the relationships between nodes
    and differentiating street lights with a different color. This version ensures that all neighbor
    relationships are displayed.
    """
    G = nx.Graph()  # Usamos Graph para representar todas las relaciones de vecindad

    # Añadir nodos al grafo con posiciones
    for node in nodes:
        G.add_node(node.get_id(), pos=(node.x, node.y))

    # Añadir aristas para todas las relaciones de vecindad dentro del dominio
    domain_nodes = domain.get_nodes()
    
    for node in domain_nodes:
        for neighbor in node.neighbors:
            if neighbor in domain_nodes:  # Solo agregar si el vecino está en el mismo dominio
                G.add_edge(node.get_id(), neighbor.get_id())

    # Posiciones de los nodos para el layout del gráfico
    pos = nx.get_node_attributes(G, 'pos')

    # Identificar street lights dentro del dominio
    street_lights = [node for node in domain_nodes if isinstance(node, StreetLight)]
    other_nodes = [node for node in domain_nodes if not isinstance(node, StreetLight)]

    # Dibujar street lights del dominio en amarillo
    street_light_ids = [node.get_id() for node in street_lights]
    nx.draw_networkx_nodes(G, pos, nodelist=street_light_ids, node_size=300, node_color='yellow', label=f'Street Lights')

    # Dibujar otros nodos del dominio en rojo
    other_node_ids = [node.get_id() for node in other_nodes]
    nx.draw_networkx_nodes(G, pos, nodelist=other_node_ids, node_size=300, node_color='red', label=f'Other Nodes')
    
    # Dibujar aristas (relaciones de vecindad) dentro del dominio
    nx.draw_networkx_edges(G, pos, edgelist=G.edges())

    # Dibujar labels de todos los nodos
    nx.draw_networkx_labels(G, pos, labels={node.get_id(): node.get_id() for node in domain_nodes})
    
    # Título del gráfico
    plt.title(f'DODAG Network for Domain {domain_index}')
    
    # Mostrar leyenda
    plt.legend()
    
    # Mostrar gráfico
    plt.show()

