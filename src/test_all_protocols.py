import argparse
import random
import simpy

from protocols import rpl_multicast, rpl_operation, rpl_operation_second_approach, rpl_projected_routes
from network import create_network_with_spanning_tree, plot_network
from street_light import StreetLight

def send_to_all_street_lights(tx_range, num_nodes, num_street_lights, verbose=False):
    env = simpy.Environment()

    # Create the network
    nodes, positions = create_network_with_spanning_tree(env, num_nodes, num_street_lights, tx_range, verbose)
    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    # Run the simulation
    env.run(until=30)

    if verbose:
        print()

        for node in nodes:
            node.print_node_details()

        print()

    origin_node = random.choice(street_lights)
    if verbose:
        print(f"Street light {origin_node.id} sending messages to all other street lights\n")

    total_hops_rpl, hops_to_root_rpl, hops_from_root_rpl = rpl_operation(street_lights, origin_node, verbose)
    total_hops_rpl_second, hops_to_root_rpl_second, hops_from_root_rpl_second = rpl_operation_second_approach(street_lights, origin_node, verbose)
    total_hops_projected_routes = rpl_projected_routes(street_lights, origin_node, verbose)
    total_hops_multicast = rpl_multicast(origin_node, street_lights, verbose)
    
    print(f"Standard RPL Operation: {total_hops_rpl}, {hops_to_root_rpl}, {hops_from_root_rpl}")
    print(f"Standard RPL Operation alternative: {total_hops_rpl_second}, {hops_to_root_rpl_second}, {hops_from_root_rpl_second}")
    print(f"RPL Projected Routes: {total_hops_projected_routes}")
    print(f"Proposed Solution: {total_hops_multicast}")

    # Plot the resulting DODAG
    if verbose:
        plot_network(nodes, positions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send messages to all street lights in a network simulation.")
    parser.add_argument('--tx_range', type=int, default=30, help='Transmission range for each node')
    parser.add_argument('--num_nodes', type=int, default=10, help='Total number of nodes in the network')
    parser.add_argument('--num_street_lights', type=int, default=3, help='Number of street lights')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    send_to_all_street_lights(args.tx_range, args.num_nodes, args.num_street_lights, args.verbose)
