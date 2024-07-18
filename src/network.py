import random
import matplotlib.pyplot as plt
import networkx as nx
from mpl_domain import MPL_Domain
from node import Node
from street_light import StreetLight
from track import Track

def create_network(env, num_nodes, tx_range):
    nodes = [Node(env, i, tx_range) for i in range(num_nodes)]
    
    # Randomly place nodes in a 2D space and find neighbors within tx_range
    positions = {node.id: (random.uniform(0, 70), random.uniform(0, 70)) for node in nodes}
    for node in nodes:
        node_pos = positions[node.id]
        for other_node in nodes:
            if other_node.id != node.id:
                other_pos = positions[other_node.id]
                distance = ((node_pos[0] - other_pos[0]) ** 2 + (node_pos[1] - other_pos[1]) ** 2) ** 0.5
                if distance <= node.tx_range:
                    node.neighbors.append(other_node)
    
    root_node = random.choice(nodes)
    root_node.set_as_root()

    # Verificar y asignar preferred_parent si falta
    for node in nodes:
        if not node.is_root and node.preferred_parent is None:
            potential_parents = [neighbor for neighbor in node.neighbors if neighbor.rank is not None]
            if potential_parents:
                node.preferred_parent = random.choice(potential_parents)
                node.preferred_parent.children.append(node)
                print(f"Node {node.id} assigned random preferred parent Node {node.preferred_parent.id}")

    return nodes, positions


# Function to find a random node within max_distance from current street lights
def find_random_node_within_distance(nodes, indices, positions, max_distance):
    potential_nodes = []
    for idx in indices:
        node_pos = positions[idx]
        for node in nodes:
            if node.id not in indices:
                other_pos = positions[node.id]
                distance = ((node_pos[0] - other_pos[0]) ** 2 + (node_pos[1] - other_pos[1]) ** 2) ** 0.5
                if distance <= max_distance:
                    potential_nodes.append(node)
    return random.choice(potential_nodes) if potential_nodes else None


def add_nodes_to_mpl_domain(mpl_domain, nodes, verbose):
    # Add street lights and necessary relay nodes to MPL Domain
    for street_light in [node for node in nodes if isinstance(node, StreetLight)]:
        mpl_domain.add_node(street_light, verbose)

    # Ensure all street lights can communicate within the MPL Domain
    for street_light in [node for node in nodes if isinstance(node, StreetLight)]:
        for other_node in nodes:
            if street_light != other_node and other_node not in mpl_domain.nodes:
                shortest_path = street_light.compute_shortest_path_to_destination(other_node.id)
                if shortest_path:
                    for path_node in shortest_path:
                        mpl_domain.add_node(path_node, verbose)

    if verbose:
        print(f"MPL Domain: {mpl_domain}")


def create_network_with_mpl_domain(env, num_nodes, num_street_lights, tx_range, verbose):
    nodes = [Node(env, i, tx_range, verbose) for i in range(num_nodes)]

    mpl_domain_address = "MPL_Domain_1"
    mpl_domain = MPL_Domain(1, mpl_domain_address)

    # Create a grid of positions to ensure connectivity
    grid_size = int((num_nodes ** 0.5) * 2)  # Grid size to ensure nodes are within range
    positions = {node.id: (random.uniform(0, 70), random.uniform(0, 70)) for node in nodes}

    # Randomly select the first street light
    street_light_indices = [random.randint(0, num_nodes - 1)]
    nodes[street_light_indices[0]] = StreetLight(env, street_light_indices[0], tx_range, mpl_domain_address)

    # Select the remaining street lights ensuring connectivity
    max_distance = tx_range  # Use the transmission range as the max distance
    while len(street_light_indices) < num_street_lights:
        nearest_node = find_random_node_within_distance(nodes, street_light_indices, positions, max_distance)
        if nearest_node:
            nodes[nearest_node.id] = StreetLight(env, nearest_node.id, tx_range, mpl_domain_address)
            street_light_indices.append(nearest_node.id)
        else:
            remaining_indices = [i for i in range(num_nodes) if i not in street_light_indices]
            nearest_node_idx = random.choice(remaining_indices)
            nodes[nearest_node_idx] = StreetLight(env, nearest_node_idx, tx_range, mpl_domain_address)
            street_light_indices.append(nearest_node_idx)
    
    # Assign neighbors based on tx_range
    for node in nodes:
        node_pos = positions[node.id]
        for other_node in nodes:
            if other_node.id != node.id:
                other_pos = positions[other_node.id]
                distance = ((node_pos[0] - other_pos[0]) ** 2 + (node_pos[1] - other_pos[1]) ** 2) ** 0.5
                if distance <= node.tx_range:
                    node.neighbors.append(other_node)
    
    # Randomly select a root node that is not a street light
    root_node_idx = random.choice([i for i in range(num_nodes) if i not in street_light_indices])
    root_node = nodes[root_node_idx]
    root_node.set_as_root(verbose)

    # Assign preferred parents to ensure all nodes have a parent
    for node in nodes:
        if not node.is_root and node.preferred_parent is None:
            potential_parents = [neighbor for neighbor in node.neighbors if neighbor.rank is not None]
            if potential_parents:
                node.preferred_parent = random.choice(potential_parents)
                node.preferred_parent.children.append(node)
                if verbose: print(f"Node {node.id} assigned random preferred parent Node {node.preferred_parent.id}")

    # Ensure street lights have a parent
    for sl_idx in street_light_indices:
        street_light = nodes[sl_idx]
        if street_light.preferred_parent is None:
            potential_parents = [neighbor for neighbor in street_light.neighbors if neighbor.rank is not None]
            if potential_parents:
                street_light.preferred_parent = random.choice(potential_parents)
                street_light.preferred_parent.children.append(street_light)
                if verbose: print(f"Street light {street_light.id} assigned random preferred parent Node {street_light.preferred_parent.id}")
                        
    add_nodes_to_mpl_domain(mpl_domain, nodes, verbose)

    # Use NetworkX spring layout for better node positioning
    G = nx.Graph()
    for node in nodes:
        G.add_node(node.id)
        for neighbor in node.neighbors:
            G.add_edge(node.id, neighbor.id)

    pos = nx.spring_layout(G)

    # Convert NetworkX positions to a dictionary compatible with plot_dodag
    positions = {node_id: pos[node_id] for node_id in pos}

    return nodes, positions

def create_network_with_mpl_domain(env, num_nodes, num_street_lights, tx_range, verbose):
    nodes = [Node(env, i, tx_range, verbose) for i in range(num_nodes)]

    mpl_domain_address = "MPL_Domain_1"
    mpl_domain = MPL_Domain(1, mpl_domain_address)
    
    # Randomly select the first street light
    street_light_indices = [random.randint(0, num_nodes - 1)]
    nodes[street_light_indices[0]] = StreetLight(env, street_light_indices[0], tx_range, mpl_domain_address)

    # Randomly place nodes in a 2D space
    positions = {node.id: (random.uniform(0, 70), random.uniform(0, 70)) for node in nodes}

    # Select the remaining street lights within a certain range of the previous ones
    max_distance = 30  # Define the maximum distance allowed for the next street light
    while len(street_light_indices) < num_street_lights:
        nearest_node = find_random_node_within_distance(nodes, street_light_indices, positions, max_distance)
        if nearest_node:
            nodes[nearest_node.id] = StreetLight(env, nearest_node.id, tx_range, mpl_domain_address)
            street_light_indices.append(nearest_node.id)
        else:
            # If no node is found within the max_distance, select one randomly
            remaining_indices = [i for i in range(num_nodes) if i not in street_light_indices]
            nearest_node_idx = random.choice(remaining_indices)
            nodes[nearest_node_idx] = StreetLight(env, nearest_node_idx, tx_range, mpl_domain_address)
            street_light_indices.append(nearest_node_idx)
    
    # Assign neighbors based on tx_range after all nodes have been created and positioned
    for node in nodes:
        node_pos = positions[node.id]
        for other_node in nodes:
            if other_node.id != node.id:
                other_pos = positions[other_node.id]
                distance = ((node_pos[0] - other_pos[0]) ** 2 + (node_pos[1] - other_pos[1]) ** 2) ** 0.5
                if distance <= node.tx_range:
                    node.neighbors.append(other_node)
    
    # Randomly select a root node that is not a street light
    root_node_idx = random.choice([i for i in range(num_nodes) if i not in street_light_indices])
    root_node = nodes[root_node_idx]
    root_node.set_as_root(verbose)

    # Assign preferred parents if not set
    for node in nodes:
        if not node.is_root and node.preferred_parent is None:
            potential_parents = [neighbor for neighbor in node.neighbors if neighbor.rank is not None]
            if potential_parents:
                node.preferred_parent = random.choice(potential_parents)
                node.preferred_parent.children.append(node)
                if verbose: print(f"Node {node.id} assigned random preferred parent Node {node.preferred_parent.id}")

    add_nodes_to_mpl_domain(mpl_domain, nodes, verbose)
                        
    return nodes, positions


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


def create_network_with_tracks(env, num_nodes, num_street_lights, tx_range, verbose):
    nodes = [Node(env, i, tx_range, verbose) for i in range(num_nodes)]

    # Create a grid of positions to ensure connectivity
    grid_size = int((num_nodes ** 0.5) * 2)  # Grid size to ensure nodes are within range
    positions = {node.id: (random.uniform(0, 70), random.uniform(0, 70)) for node in nodes}

    # Randomly select the first street light
    street_light_indices = [random.randint(0, num_nodes - 1)]
    nodes[street_light_indices[0]] = StreetLight(env, street_light_indices[0], tx_range)

    # Select the remaining street lights ensuring connectivity
    max_distance = tx_range  # Use the transmission range as the max distance
    while len(street_light_indices) < num_street_lights:
        nearest_node = find_random_node_within_distance(nodes, street_light_indices, positions, max_distance)
        if nearest_node:
            nodes[nearest_node.id] = StreetLight(env, nearest_node.id, tx_range)
            street_light_indices.append(nearest_node.id)
        else:
            remaining_indices = [i for i in range(num_nodes) if i not in street_light_indices]
            nearest_node_idx = random.choice(remaining_indices)
            nodes[nearest_node_idx] = StreetLight(env, nearest_node_idx, tx_range)
            street_light_indices.append(nearest_node_idx)
    
    # Assign neighbors based on tx_range
    for node in nodes:
        node_pos = positions[node.id]
        for other_node in nodes:
            if other_node.id != node.id:
                other_pos = positions[other_node.id]
                distance = ((node_pos[0] - other_pos[0]) ** 2 + (node_pos[1] - other_pos[1]) ** 2) ** 0.5
                if distance <= node.tx_range:
                    node.neighbors.append(other_node)
    
    # Randomly select a root node that is not a street light
    root_node_idx = random.choice([i for i in range(num_nodes) if i not in street_light_indices])
    root_node = nodes[root_node_idx]
    root_node.set_as_root(verbose)

    # Assign preferred parents to ensure all nodes have a parent
    for node in nodes:
        if not node.is_root and node.preferred_parent is None:
            potential_parents = [neighbor for neighbor in node.neighbors if neighbor.rank is not None]
            if potential_parents:
                node.preferred_parent = random.choice(potential_parents)
                node.preferred_parent.children.append(node)
                if verbose: print(f"Node {node.id} assigned random preferred parent Node {node.preferred_parent.id}")

    # Ensure street lights have a parent
    for sl_idx in street_light_indices:
        street_light = nodes[sl_idx]
        if street_light.preferred_parent is None:
            potential_parents = [neighbor for neighbor in street_light.neighbors if neighbor.rank is not None]
            if potential_parents:
                street_light.preferred_parent = random.choice(potential_parents)
                street_light.preferred_parent.children.append(street_light)
                if verbose: print(f"Street light {street_light.id} assigned random preferred parent Node {street_light.preferred_parent.id}")
                        
    compute_tracks(nodes, verbose)

    # Use NetworkX spring layout for better node positioning
    G = nx.Graph()
    for node in nodes:
        G.add_node(node.id)
        for neighbor in node.neighbors:
            G.add_edge(node.id, neighbor.id)

    pos = nx.spring_layout(G)

    # Convert NetworkX positions to a dictionary compatible with plot_dodag
    positions = {node_id: pos[node_id] for node_id in pos}

    return nodes, positions


## MIXTURE OF ALL


def create_network_with_mpl_domain_and_tracks(env, num_nodes, num_street_lights, tx_range, verbose):
    nodes = [Node(env, i, tx_range, verbose) for i in range(num_nodes)]

    mpl_domain_address = "MPL_Domain_1"
    mpl_domain = MPL_Domain(1, mpl_domain_address)

    # Create a grid of positions to ensure connectivity
    grid_size = int((num_nodes ** 0.5) * 2)  # Grid size to ensure nodes are within range
    positions = {node.id: (random.uniform(0, 70), random.uniform(0, 70)) for node in nodes}

    # Randomly select the first street light
    street_light_indices = [random.randint(0, num_nodes - 1)]
    nodes[street_light_indices[0]] = StreetLight(env, street_light_indices[0], tx_range, mpl_domain_address)

    # Select the remaining street lights ensuring connectivity
    max_distance = tx_range  # Use the transmission range as the max distance
    while len(street_light_indices) < num_street_lights:
        nearest_node = find_random_node_within_distance(nodes, street_light_indices, positions, max_distance)
        if nearest_node:
            nodes[nearest_node.id] = StreetLight(env, nearest_node.id, tx_range, mpl_domain_address)
            street_light_indices.append(nearest_node.id)
        else:
            remaining_indices = [i for i in range(num_nodes) if i not in street_light_indices]
            nearest_node_idx = random.choice(remaining_indices)
            nodes[nearest_node_idx] = StreetLight(env, nearest_node_idx, tx_range, mpl_domain_address)
            street_light_indices.append(nearest_node_idx)
    
    # Assign neighbors based on tx_range
    for node in nodes:
        node_pos = positions[node.id]
        for other_node in nodes:
            if other_node.id != node.id:
                other_pos = positions[other_node.id]
                distance = ((node_pos[0] - other_pos[0]) ** 2 + (node_pos[1] - other_pos[1]) ** 2) ** 0.5
                if distance <= node.tx_range:
                    node.neighbors.append(other_node)
    
    # Randomly select a root node that is not a street light
    root_node_idx = random.choice([i for i in range(num_nodes) if i not in street_light_indices])
    root_node = nodes[root_node_idx]
    root_node.set_as_root(verbose)

    # Assign preferred parents to ensure all nodes have a parent
    for node in nodes:
        if not node.is_root and node.preferred_parent is None:
            potential_parents = [neighbor for neighbor in node.neighbors if neighbor.rank is not None]
            if potential_parents:
                node.preferred_parent = random.choice(potential_parents)
                node.preferred_parent.children.append(node)
                if verbose: print(f"Node {node.id} assigned random preferred parent Node {node.preferred_parent.id}")

    # Ensure street lights have a parent
    for sl_idx in street_light_indices:
        street_light = nodes[sl_idx]
        if street_light.preferred_parent is None:
            potential_parents = [neighbor for neighbor in street_light.neighbors if neighbor.rank is not None]
            if potential_parents:
                street_light.preferred_parent = random.choice(potential_parents)
                street_light.preferred_parent.children.append(street_light)
                if verbose: print(f"Street light {street_light.id} assigned random preferred parent Node {street_light.preferred_parent.id}")
                        
    add_nodes_to_mpl_domain(mpl_domain, nodes, verbose)
    compute_tracks(nodes, verbose)

    # Use NetworkX spring layout for better node positioning
    G = nx.Graph()
    for node in nodes:
        G.add_node(node.id)
        for neighbor in node.neighbors:
            G.add_edge(node.id, neighbor.id)

    pos = nx.spring_layout(G)

    # Convert NetworkX positions to a dictionary compatible with plot_dodag
    positions = {node_id: pos[node_id] for node_id in pos}

    return nodes, positions


#### MINIMUM SPANNING TREE


def create_network_with_spanning_tree(env, num_nodes, num_street_lights, tx_range, verbose):
    mpl_domain_address = "MPL_Domain_1"
    mpl_domain = MPL_Domain(1, mpl_domain_address)

    nodes = [Node(env, i, tx_range, verbose) for i in range(num_nodes)]

    # Create a complete graph with random weights
    G = nx.complete_graph(num_nodes)
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = random.uniform(1, 10)  # Assign random weights for simulation purposes

    # Compute the Minimum Spanning Tree (MST)
    T = nx.minimum_spanning_tree(G, weight='weight')

    # Assign neighbors based on the MST
    for u, v in T.edges():
        nodes[u].neighbors.append(nodes[v])
        nodes[v].neighbors.append(nodes[u])

    # Randomly select the street lights ensuring they are part of the spanning tree
    street_light_indices = random.sample(range(num_nodes), num_street_lights)
    for idx in street_light_indices:
        nodes[idx] = StreetLight(env, idx, tx_range, mpl_domain_address)

    # Randomly select a root node that is not a street light
    root_node_idx = random.choice([i for i in range(num_nodes) if i not in street_light_indices])
    root_node = nodes[root_node_idx]
    root_node.set_as_root(verbose)

    # Assign preferred parents based on the MST structure
    parent_map = nx.predecessor(T, root_node_idx)
    for node in nodes:
        if not node.is_root:
            parent_id = parent_map[node.id][0] if parent_map[node.id] else None
            if parent_id is not None:
                parent_node = nodes[parent_id]
                node.preferred_parent = parent_node
                parent_node.children.append(node)
                if verbose:
                    print(f"Node {node.id} assigned preferred parent Node {node.preferred_parent.id}")

    add_nodes_to_mpl_domain(mpl_domain, nodes, verbose)
    compute_tracks(nodes, verbose)

    return nodes, T

def plot_network(nodes, T):
    G = nx.Graph()

    for node in nodes:
        G.add_node(node.id)
        for neighbor in node.neighbors:
            G.add_edge(node.id, neighbor.id)

    pos = nx.spring_layout(G)

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    
    # Highlight the MST
    mst_edges = list(T.edges())
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=2, edge_color='blue')

    # Highlight the root
    root_nodes = [node.id for node in nodes if node.is_root]
    nx.draw_networkx_nodes(G, pos, nodelist=root_nodes, node_color='green', node_size=700)

    # Highlight the street lights
    street_light_nodes = [node.id for node in nodes if isinstance(node, StreetLight)]
    nx.draw_networkx_nodes(G, pos, nodelist=street_light_nodes, node_color='orange', node_size=700)

    plt.title("Network with MST Highlighted")
    plt.show()

#############


def plot_basic_dodag(nodes, positions):
    street_light_label_plotted = False
    dodag_link_label_plotted = False
    non_dodag_link_label_plotted = False

    plt.figure(figsize=(10, 10))
    for node in nodes:
        x, y = positions[node.id]
        if isinstance(node, StreetLight):
            if not street_light_label_plotted: 
                plt.scatter(x, y, c='red', s=100, label='Street Light')
                street_light_label_plotted = True
            else:
                plt.scatter(x, y, c='red', s=100)
        elif node.is_dodag_root():
            plt.scatter(x, y, c='magenta', s=100, label='Root')
        else:
            plt.scatter(x, y, c='blue' if not node.is_dodag_root() else 'red', s=100)
        plt.text(x, y, f' {node.id}', fontsize=12)
        for neighbor in node.neighbors:
            nx, ny = positions[neighbor.id]
            if not non_dodag_link_label_plotted:
                plt.plot([x, nx], [y, ny], 'k-', lw=0.5, label='Non-DODAG Link')
                non_dodag_link_label_plotted = True
            else:
                plt.plot([x, nx], [y, ny], 'k-', lw=0.5)
            if neighbor.rank is not None and neighbor.rank == node.rank + 1:
                if not  dodag_link_label_plotted: 
                    plt.plot([x, nx], [y, ny], 'g-', lw=1.5, label='DODAG Link')
                    dodag_link_label_plotted = True
                else:
                    plt.plot([x, nx], [y, ny], 'g-', lw=1.5)
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('DODAG Visualization')
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_dodag(nodes, positions):
    # Create a graph for plotting
    G = nx.Graph()

    # Add nodes to the graph
    for node in nodes:
        G.add_node(node.id)

    # Add edges between nodes based on neighbor relationships
    for node in nodes:
        for neighbor in node.neighbors:
            G.add_edge(node.id, neighbor.id)

    # Initialize levels dictionary to store levels of each node
    levels = {}

    def assign_levels(node_id, current_level):
        if node_id not in levels or current_level < levels[node_id]:
            levels[node_id] = current_level
            for neighbor in G.neighbors(node_id):
                if levels[node_id] + 1 < levels.get(neighbor, float('inf')):
                    assign_levels(neighbor, current_level + 1)

    # Assign levels starting from the root
    for node in nodes:
        if node.is_root:
            assign_levels(node.id, 0)

    # Create a dictionary to store adjusted positions
    adjusted_positions = {}
    for node_id, (x, y) in positions.items():
        level = levels.get(node_id, float('inf'))
        adjusted_positions[node_id] = (x, -level)  # Invert the level to ensure proper ordering

    # Plotting the graph
    plt.figure(figsize=(12, 12))

    # Plot nodes
    street_light_label_plotted = False
    dodag_link_label_plotted = False
    non_dodag_link_label_plotted = False

    for node in nodes:
        x, y = adjusted_positions[node.id]
        if isinstance(node, StreetLight):
            if not street_light_label_plotted:
                plt.scatter(x, y, c='red', s=100, label='Street Light')
                street_light_label_plotted = True
            else:
                plt.scatter(x, y, c='red', s=100)
        elif node.is_root:
            plt.scatter(x, y, c='magenta', s=100, label='Root')
        else:
            plt.scatter(x, y, c='blue', s=100)

        plt.text(x, y, f' {node.id}', fontsize=12)

        for neighbor in node.neighbors:
            n_x, n_y = adjusted_positions[neighbor.id]
            if not non_dodag_link_label_plotted:
                plt.plot([x, n_x], [y, n_y], 'k-', lw=0.5, label='Non-DODAG Link')
                non_dodag_link_label_plotted = True
            else:
                plt.plot([x, n_x], [y, n_y], 'k-', lw=0.5)

            if neighbor.rank is not None and neighbor.rank == node.rank + 1:
                if not dodag_link_label_plotted:
                    plt.plot([x, n_x], [y, n_y], 'g-', lw=1.5, label='DODAG Link')
                    dodag_link_label_plotted = True
                else:
                    plt.plot([x, n_x], [y, n_y], 'g-', lw=1.5)

    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('DODAG Visualization')
    plt.grid(True)
    plt.legend()
    plt.show()