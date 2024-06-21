import simpy
import random
from network import create_network, plot_dodag
from message import Message

def main():
    env = simpy.Environment()
    tx_range = 40  # Increased transmission range for each node
    num_nodes = 20 # Total number of nodes in the network

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
    main()
