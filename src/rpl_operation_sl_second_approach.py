import simpy
import random
from network import create_network_with_mpl_domain, plot_dodag
from message import Message
from street_light import StreetLight

def main_send_to_all_street_lights():
    env = simpy.Environment()
    tx_range = 30  # Increased transmission range for each node
    num_nodes = 10 # Total number of nodes in the network
    num_street_lights = 3  # Number of street lights

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
    message = Message(origin_node.id, destination, "Movement Alert")
    origin_node.send_message_upwards(message)
    
    print()

    message.print_route()

    # Plot the resulting DODAG
    plot_dodag(nodes, positions)

if __name__ == "__main__":
    main_send_to_all_street_lights()