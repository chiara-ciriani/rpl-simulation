import simpy
import random
import matplotlib.pyplot as plt
from node import Node
from street_light import StreetLight

def create_network(env, num_nodes, num_street_lights, tx_range):
    nodes = [Node(env, i, tx_range) for i in range(num_nodes)]
    
    # Randomly select nodes to be street lights
    street_light_indices = random.sample(range(num_nodes), num_street_lights)
    for idx in street_light_indices:
        nodes[idx] = StreetLight(env, idx, tx_range)
    
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
    
    # Randomly select a root node that is not a street light
    root_node_idx = random.choice([i for i in range(num_nodes) if i not in street_light_indices])
    root_node = nodes[root_node_idx]
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