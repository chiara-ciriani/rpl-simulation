import argparse
import random
import simpy

from mpl_domain import MPL_Domain
from street_light import StreetLight

from protocols import rpl_multicast, rpl_operation, rpl_operation_second_approach, rpl_projected_routes

from creating_domains import compute_tracks, create_network_with_spanning_tree, plot_network, add_nodes_to_mpl_domain_disjoint_path, add_street_light_to_mpl_domain

def send_to_all_street_lights(num_nodes, num_street_lights, tx_range, max_distance, verbose=False):
    env = simpy.Environment()

    # Crear la red y el árbol de expansión mínima
    nodes, T, root = create_network_with_spanning_tree(env, num_nodes, num_street_lights, tx_range, max_distance, verbose)
    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    # Agregar nodos al dominio MPL

    mpl_domain_address_1 = "MPL_Domain_1"
    mpl_domain_1 = MPL_Domain(1, mpl_domain_address_1)
    add_nodes_to_mpl_domain_disjoint_path(mpl_domain_1, nodes, T, verbose)

    mpl_domain_address_2 = "MPL_Domain_2"
    mpl_domain_2 = MPL_Domain(2, mpl_domain_address_2)
    add_street_light_to_mpl_domain(mpl_domain_2, nodes, verbose)

    # Compute tracks
    compute_tracks(nodes, verbose)

    # Run the simulation
    env.run(until=30)

    results = {}

    for street_light in street_lights:
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

        print(f"Standard RPL Operation: {total_hops_rpl}, {hops_to_root_rpl}, {hops_from_root_rpl}")
        print(f"Standard RPL Operation alternative: {total_hops_rpl_second}, {hops_to_root_rpl_second}, {hops_from_root_rpl_second}")
        print(f"RPL Projected Routes: {total_hops_projected_routes}")
        print(f"Proposed Solution with Domain 1: {total_hops_domain1}")
        print(f"Proposed Solution with Domain 2: {total_hops_domain2}\n")

        print("")

        results[street_light.get_id()] = [total_hops_rpl, total_hops_rpl_second, total_hops_projected_routes, total_hops_domain1, total_hops_domain2]

    print(results)
    print((f"Root position: {root.x}, {root.y}"))

    # Visualizar la red
    plot_network(nodes, T, mpl_domain_1, mpl_domain_2)


MAX_DISTANCE = 10  # Distancia máxima entre street lights

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send messages to all street lights in a network simulation.")
    parser.add_argument('--tx_range', type=int, default=20, help='Transmission range for each node')
    parser.add_argument('--num_nodes', type=int, default=50, help='Total number of nodes in the network')
    parser.add_argument('--num_street_lights', type=int, default=5, help='Number of street lights')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    send_to_all_street_lights(args.num_nodes, args.num_street_lights, args.tx_range, MAX_DISTANCE, args.verbose)


