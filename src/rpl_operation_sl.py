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

    routes = []

    for street_light in street_lights:
        if street_light != origin_node:
            message = Message(origin_node.id, street_light.id, "RPL Message")
            origin_node.send_message_upwards(message)
            routes.append(message.get_route())
    
    print()

    print(f"Routes: {[[node.id for node in route] for route in routes]}")

    # Plot the resulting DODAG
    plot_dodag(nodes, positions)

if __name__ == "__main__":
    main_send_to_all_street_lights()