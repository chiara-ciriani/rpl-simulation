import argparse
import simpy

from mpl_domain import MPL_Domain
from street_light import StreetLight

from creating_domains_dio import add_nodes_to_multipath_domain, add_nodes_to_multipath_domain_common_neighbors, compute_tracks_multipath, compute_tracks_multipath_disjoint_paths, create_network_with_dio, plot_network

from calculate_prob_bf import brute_force_solution
from calculate_prob_mc import monte_carlo_simulation

STREET_LIGHT_INDEXES = [0, 5, 10]
NUM_STREET_LIGHTS=11

NUM_SIMULATIONS=1000

def calculate_latency(width, height, num_nodes, num_street_lights, tx_range, max_distance, verbose=False):
    env = simpy.Environment()

    # Crear la red 
    nodes, root = create_network_with_dio(env, width, height, num_nodes, num_street_lights, tx_range, max_distance, verbose)
    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    # Compute tracks
    track_nodes = compute_tracks_multipath(nodes, verbose)
    track_nodes2 = compute_tracks_multipath_disjoint_paths(nodes, verbose)

    # Agregar nodos al dominio MPL
    mpl_domain_address_1 = "MPL_Domain_1"
    mpl_domain_1 = MPL_Domain(1, mpl_domain_address_1)
    add_nodes_to_multipath_domain(mpl_domain_1, track_nodes, verbose)

    mpl_domain_address_2 = "MPL_Domain_2"
    mpl_domain_2 = MPL_Domain(2, mpl_domain_address_2)
    add_nodes_to_multipath_domain_common_neighbors(mpl_domain_2, nodes, verbose)

    mpl_domain_address_3 = "MPL_Domain_3"
    mpl_domain_3 = MPL_Domain(3, mpl_domain_address_3)
    add_nodes_to_multipath_domain(mpl_domain_3, track_nodes2, verbose)

    # Run the simulation
    env.run(until=30)

    results = {}

    # Probabilidades para cada origen
    for source_id in STREET_LIGHT_INDEXES:
        destination_ids = [light.id for light in street_lights if light.id != source_id]

        _, latency_mc_domain1 = monte_carlo_simulation(mpl_domain_1.get_nodes(), source_id, destination_ids, NUM_SIMULATIONS)
        _, latency_mc_domain2 = monte_carlo_simulation(mpl_domain_2.get_nodes(), source_id, destination_ids, NUM_SIMULATIONS)
        _, latency_mc_domain3 = monte_carlo_simulation(mpl_domain_3.get_nodes(), source_id, destination_ids, NUM_SIMULATIONS)

        results[f'latency_mc_domain1_source_{source_id}'] = latency_mc_domain1
        results[f'latency_mc_domain2_source_{source_id}'] = latency_mc_domain2
        results[f'latency_mc_domain3_source_{source_id}'] = latency_mc_domain3

    if verbose:
        for source_id in STREET_LIGHT_INDEXES:
            print(f"Domain 1 Monte Carlo (Source {source_id}): {results[f'latency_mc_domain1_source_{source_id}']}")
            print(f"Domain 2 Monte Carlo (Source {source_id}): {results[f'latency_mc_domain2_source_{source_id}']}")
            print(f"Domain 3 Monte Carlo (Source {source_id}): {results[f'latency_mc_domain3_source_{source_id}']}")
        
        plot_network(nodes, mpl_domain_1, mpl_domain_2, mpl_domain_3)

    return results


MAX_DISTANCE = 5  # Distancia máxima entre street lights

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send messages to all street lights in a network simulation.")
    parser.add_argument('--tx_range', type=int, default=5, help='Transmission range for each node')
    parser.add_argument('--width', type=int, default=20, help='Width of the network')
    parser.add_argument('--height', type=int, default=20, help='Height of the network')
    parser.add_argument('--num_nodes', type=int, default=20, help='Total number of nodes in the network')
    parser.add_argument('--num_street_lights', type=int, default=3, help='Number of street lights')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    calculate_latency(args.width, args.height, args.num_nodes, args.num_street_lights, args.tx_range, MAX_DISTANCE, args.verbose)


