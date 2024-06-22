import argparse
import random
import simpy

from message import Message
from network import create_network, plot_dodag

def send_message_using_rpl_operation(tx_range, num_nodes):
    env = simpy.Environment()

    # Create the network
    nodes, positions = create_network(env, num_nodes, tx_range)
    
    # Run the simulation
    env.run(until=20)

    print()

    for node in nodes:
        node.print_node_details()

    print()

    # Seleccionar un nodo aleatorio como nodo origen
    origin_node = random.choice(nodes)

     # Elegir un destino aleatorio diferente al origen
    destinations = [node.id for node in nodes if node.id != origin_node.id]
    destination = random.choice(destinations)

    print(f"Sending message from Node {origin_node.id} to Node {destination}\n")
 
    # Crear el mensaje
    message = Message(origin_node.id, destination, "Hello, world!")
 
    # Simular el envío del mensaje desde el nodo origen
    origin_node.send_message_upwards(message)

    print()

    print(f"Route: {message.print_route()}")
    
    # Plot the resulting DODAG
    plot_dodag(nodes, positions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send messages to random node in a network simulation using RPL Operation.")
    parser.add_argument('--tx_range', type=int, default=40, help='Transmission range for each node')
    parser.add_argument('--num_nodes', type=int, default=20, help='Total number of nodes in the network')

    args = parser.parse_args()

    send_message_using_rpl_operation(args.tx_range, args.num_nodes)
