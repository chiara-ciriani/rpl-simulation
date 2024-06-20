import random
import matplotlib.pyplot as plt
from mpl_domain import MPL_Domain
from node import Node
from street_light import StreetLight

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
def find_random_node_within_distance(nodes, current_nodes, positions, max_distance):
    potential_nodes = []
    for node in nodes:
        if node.id not in current_nodes:
            for idx in current_nodes:
                distance = ((positions[node.id][0] - positions[idx][0]) ** 2 + (positions[node.id][1] - positions[idx][1]) ** 2) ** 0.5
                if distance < max_distance:
                    potential_nodes.append(node)
    if potential_nodes:
        return random.choice(potential_nodes)
    else:
        return None

def create_network_with_mpl_domain(env, num_nodes, num_street_lights, tx_range):
    nodes = [Node(env, i, tx_range) for i in range(num_nodes)]

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
    root_node.set_as_root()

    # Assign preferred parents if not set
    for node in nodes:
        if not node.is_root and node.preferred_parent is None:
            potential_parents = [neighbor for neighbor in node.neighbors if neighbor.rank is not None]
            if potential_parents:
                node.preferred_parent = random.choice(potential_parents)
                node.preferred_parent.children.append(node)
                print(f"Node {node.id} assigned random preferred parent Node {node.preferred_parent.id}")

    # Add street lights and necessary relay nodes to MPL Domain
    for street_light in [node for node in nodes if isinstance(node, StreetLight)]:
        mpl_domain.add_node(street_light)

    # Ensure all street lights can communicate within the MPL Domain
    for street_light in [node for node in nodes if isinstance(node, StreetLight)]:
        for other_node in nodes:
            if street_light != other_node and other_node not in mpl_domain.nodes:
                shortest_path = street_light.compute_shortest_path_to_destination(other_node.id)
                if shortest_path:
                    for path_node in shortest_path:
                        mpl_domain.add_node(path_node)

    print(f"MPL Domain: {mpl_domain}")
                        
    return nodes, positions


def plot_dodag(nodes, positions):
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