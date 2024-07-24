import argparse
import simpy

from mpl_domain import MPL_Domain
from street_light import StreetLight

from protocols import rpl_multicast, rpl_operation, rpl_operation_second_approach, rpl_projected_routes

from creating_domains_dio import add_nodes_to_multipath_domain, add_nodes_to_multipath_domain_common_neighbors, compute_tracks_multipath, create_network_with_dio, plot_network

STREET_LIGHT_INDEXES = [0, 1, 2]
NUM_STREET_LIGHTS=3

def send_to_all_street_lights_multipath(width, height, num_nodes, num_street_lights, tx_range, max_distance, verbose=False):
    env = simpy.Environment()

    # Crear la red 
    nodes, root = create_network_with_dio(env, width, height, num_nodes, num_street_lights, tx_range, max_distance, verbose)
    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    # Compute tracks
    track_nodes = compute_tracks_multipath(nodes, verbose)

    # Agregar nodos al dominio MPL
    mpl_domain_address_1 = "MPL_Domain_1"
    mpl_domain_1 = MPL_Domain(1, mpl_domain_address_1)
    add_nodes_to_multipath_domain(mpl_domain_1, track_nodes, verbose)

    mpl_domain_address_2 = "MPL_Domain_2"
    mpl_domain_2 = MPL_Domain(2, mpl_domain_address_2)
    add_nodes_to_multipath_domain_common_neighbors(mpl_domain_2, nodes, verbose)

    # Run the simulation
    env.run(until=30)

    results = {}

    for street_light_idx in STREET_LIGHT_INDEXES:
        street_light = street_lights[street_light_idx]

        if verbose:
            street_light.print_node_details()

        origin_node = street_light
        if verbose:
            print(f"Street light {origin_node.id} sending messages to all other street lights\n")

        total_hops_rpl, hops_to_root_rpl, hops_from_root_rpl = rpl_operation(street_lights, origin_node, verbose)
        total_hops_rpl_second, hops_to_root_rpl_second, hops_from_root_rpl_second = rpl_operation_second_approach(street_lights, origin_node, verbose)
        total_hops_projected_routes = rpl_projected_routes(street_lights, origin_node, verbose)
        total_hops_domain1 = rpl_multicast(origin_node, mpl_domain_address_1, verbose)

        for node in mpl_domain_1.nodes:
            node.received_messages = []
            node.senders = []

        total_hops_domain2 = rpl_multicast(origin_node, mpl_domain_address_2, verbose)

        for node in mpl_domain_2.nodes:
            node.received_messages = []
            node.senders = []
 
        if verbose:
            print(f"Standard RPL Operation: {total_hops_rpl}, {hops_to_root_rpl}, {hops_from_root_rpl}")
            print(f"Standard RPL Operation alternative: {total_hops_rpl_second}, {hops_to_root_rpl_second}, {hops_from_root_rpl_second}")
            print(f"RPL Projected Routes: {total_hops_projected_routes}")
            print(f"Proposed Solution with Domain 1: {total_hops_domain1}")
            print(f"Proposed Solution with Domain 2: {total_hops_domain2}\n")
    
            print("")

        results[street_light.get_id()] = [total_hops_rpl, total_hops_rpl_second, total_hops_projected_routes, total_hops_domain1, total_hops_domain2]

    if verbose:
        print(results)
        print((f"Root position: {root.x}, {root.y}"))

        # Visualizar la red
        plot_network(nodes, mpl_domain_1, mpl_domain_2)

    root_position = (root.x, root.y)
    return results, root_position


MAX_DISTANCE = 10  # Distancia máxima entre street lights

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send messages to all street lights in a network simulation.")
    parser.add_argument('--tx_range', type=int, default=10, help='Transmission range for each node')
    parser.add_argument('--width', type=int, default=30, help='Width of the network')
    parser.add_argument('--height', type=int, default=30, help='Height of the network')
    parser.add_argument('--num_nodes', type=int, default=20, help='Total number of nodes in the network')
    parser.add_argument('--num_street_lights', type=int, default=3, help='Number of street lights')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    send_to_all_street_lights_multipath(args.width, args.height, args.num_nodes, args.num_street_lights, args.tx_range, MAX_DISTANCE, args.verbose)


