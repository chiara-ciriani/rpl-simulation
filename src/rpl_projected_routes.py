import simpy
import random
from network import create_network_with_tracks, plot_dodag
from message import Message
from street_light import StreetLight

def main_send_to_all_street_lights():
    env = simpy.Environment()
    tx_range = 30  # Increased transmission range for each node
    num_nodes = 10 # Total number of nodes in the network
    num_street_lights = 2  # Number of street lights

    # Create the network
    nodes, positions = create_network_with_tracks(env, num_nodes, num_street_lights, tx_range)
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
            route = origin_node.send_message_through_track(street_light.id)
            routes.append(route)
    
    print()

    print(f"Routes: {[[node.id for node in route] for route in routes]}")

    # Plot the resulting DODAG
    plot_dodag(nodes, positions)

if __name__ == "__main__":
    main_send_to_all_street_lights()