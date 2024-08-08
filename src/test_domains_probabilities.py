import argparse
import simpy

from mpl_domain import MPL_Domain
from street_light import StreetLight

from creating_domains_dio import add_nodes_to_multipath_domain, add_nodes_to_multipath_domain_common_neighbors, compute_tracks_multipath, compute_tracks_multipath_disjoint_paths, create_network_with_dio, plot_network

from calculate_prob_bf import brute_force_solution
from calculate_prob_mc import monte_carlo_simulation

STREET_LIGHT_INDEXES = [0, 5, 11]
NUM_STREET_LIGHTS=11

NUM_SIMULATIONS=1000

def calculate_probabilities(width, height, num_nodes, num_street_lights, tx_range, max_distance, verbose=False):
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

    source_id = STREET_LIGHT_INDEXES[0]
    destination_id = STREET_LIGHT_INDEXES[len(STREET_LIGHT_INDEXES) - 1]

    # probability_bf_domain1 =  brute_force_solution(mpl_domain_1.get_nodes(), source_id, destination_id)
    # probability_bf_domain2 =  brute_force_solution(mpl_domain_2.get_nodes(), source_id, destination_id)
    # probability_bf_domain3 =  brute_force_solution(mpl_domain_3.get_nodes(), source_id, destination_id)

    probability_mc_domain1 =  monte_carlo_simulation(mpl_domain_1.get_nodes(), source_id, destination_id, NUM_SIMULATIONS)
    probability_mc_domain2 =  monte_carlo_simulation(mpl_domain_2.get_nodes(), source_id, destination_id, NUM_SIMULATIONS)
    probability_mc_domain3 =  monte_carlo_simulation(mpl_domain_3.get_nodes(), source_id, destination_id, NUM_SIMULATIONS)

    # results['probability_bf_domain1'] = probability_bf_domain1
    # results['probability_bf_domain2'] = probability_bf_domain2
    # results['probability_bf_domain3'] = probability_bf_domain3
    results['probability_mc_domain1'] = probability_mc_domain1
    results['probability_mc_domain3'] = probability_mc_domain3
    results['probability_mc_domain2'] = probability_mc_domain2

    if verbose:
        # print(f"Domain 1 Brute Force: {probability_bf_domain1}")
        # print(f"Domain 2 Brute Force: {probability_bf_domain2}")
        # print(f"Domain 3 Brute Force: {probability_bf_domain3}")

        print(f"Domain 1 Monte Carlo: {probability_mc_domain1}")
        print(f"Domain 2 Monte Carlo: {probability_mc_domain2}")
        print(f"Domain 3 Monte Carlo: {probability_mc_domain3}")
        
        print(results)

        # Visualizar la red
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

    calculate_probabilities(args.width, args.height, args.num_nodes, args.num_street_lights, args.tx_range, MAX_DISTANCE, args.verbose)


