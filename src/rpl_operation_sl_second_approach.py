import argparse
import random
import simpy

from message import Message
from network import create_network_with_mpl_domain, plot_dodag
from street_light import StreetLight

def send_to_all_street_lights_using_rpl_root(tx_range, num_nodes, num_street_lights):
    env = simpy.Environment()

    # Create the network
    nodes, positions = create_network_with_mpl_domain(env, num_nodes, num_street_lights, tx_range)
    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    # Run the simulation
    env.run(until=30)

    print()

    for node in nodes:
        node.print_node_details()

    print()

    origin_node = random.choice(street_lights)
    print(f"Street light {origin_node.id} sending messages to all other street lights\n")

    # Crear una lista de todas las street lights salvo origin_node
    destination = [sl.id for sl in street_lights if sl.id != origin_node.id]

    # Enviar un solo mensaje a la raíz
    message = Message(origin_node.id, destination, "RPL Second Approach: Movement Alert!")
    origin_node.send_message_upwards(message)
    
    print()

    message.print_route()

    # Plot the resulting DODAG
    plot_dodag(nodes, positions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send messages to all street lights in a network simulation.")
    parser.add_argument('--tx_range', type=int, default=30, help='Transmission range for each node')
    parser.add_argument('--num_nodes', type=int, default=10, help='Total number of nodes in the network')
    parser.add_argument('--num_street_lights', type=int, default=3, help='Number of street lights')

    args = parser.parse_args()

    send_to_all_street_lights_using_rpl_root()