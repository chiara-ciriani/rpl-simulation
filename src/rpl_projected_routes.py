import argparse
import random
import simpy

from network import create_network_with_tracks, plot_dodag
from street_light import StreetLight

def send_to_all_street_lights_using_projected_routes(tx_range, num_nodes, num_street_lights):
    env = simpy.Environment()
    
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
    parser = argparse.ArgumentParser(description="Send messages to all street lights in a network simulation.")
    parser.add_argument('--tx_range', type=int, default=30, help='Transmission range for each node')
    parser.add_argument('--num_nodes', type=int, default=10, help='Total number of nodes in the network')
    parser.add_argument('--num_street_lights', type=int, default=2, help='Number of street lights')

    args = parser.parse_args()

    send_to_all_street_lights_using_projected_routes(args.tx_range, args.num_nodes, args.num_street_lights)