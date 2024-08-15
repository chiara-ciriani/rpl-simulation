import argparse
import simpy

from mpl_domain import MPL_Domain

from calculate_min_cut import calculate_min_cut

from creating_domains_dio import add_nodes_to_multipath_domain, add_nodes_to_multipath_domain_common_neighbors, compute_tracks_multipath, compute_tracks_multipath_disjoint_paths, create_network_with_dio, plot_network

def test_calculate_min_cut(width, height, num_nodes, num_street_lights, tx_range, max_distance, verbose=False):
    env = simpy.Environment()

    # Crear la red 
    nodes, root = create_network_with_dio(env, width, height, num_nodes, num_street_lights, tx_range, max_distance, verbose)

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

    # Calcular el corte mínimo de nodos y aristas para desconectar todo el dominio
    min_vertex_cut_domain1, min_edge_cut_domain1 = calculate_min_cut(mpl_domain_1.get_nodes())
    min_vertex_cut_domain2, min_edge_cut_domain2 = calculate_min_cut(mpl_domain_2.get_nodes())
    min_vertex_cut_domain3, min_edge_cut_domain3 = calculate_min_cut(mpl_domain_3.get_nodes())

    # Guardar resultados del min cut
    results['min_vertex_cut_domain1'] = min_vertex_cut_domain1
    results['min_edge_cut_domain1'] = min_edge_cut_domain1

    results['min_vertex_cut_domain2'] = min_vertex_cut_domain2
    results['min_edge_cut_domain2'] = min_edge_cut_domain2

    results['min_vertex_cut_domain3'] = min_vertex_cut_domain3
    results['min_edge_cut_domain3'] = min_edge_cut_domain3
    
    if verbose:
        print(f"Domain 1 Min Vertex Cut: {min_vertex_cut_domain1}")
        print(f"Domain 1 Min Edge Cut: {min_edge_cut_domain1}")

        print(f"Domain 2 Min Vertex Cut: {min_vertex_cut_domain2}")
        print(f"Domain 2 Min Edge Cut: {min_edge_cut_domain2}")

        print(f"Domain 3 Min Vertex Cut: {min_vertex_cut_domain3}")
        print(f"Domain 3 Min Edge Cut: {min_edge_cut_domain3}")

        # Visualizar la red
        plot_network(nodes, mpl_domain_1, mpl_domain_2, mpl_domain_3)

    return results


MAX_DISTANCE = 5  # Distancia máxima entre street lights

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send messages to all street lights in a network simulation.")
    parser.add_argument('--tx_range', type=int, default=5, help='Transmission range for each node')
    parser.add_argument('--width', type=int, default=65, help='Width of the network')
    parser.add_argument('--height', type=int, default=50, help='Height of the network')
    parser.add_argument('--num_nodes', type=int, default=200, help='Total number of nodes in the network')
    parser.add_argument('--num_street_lights', type=int, default=11, help='Number of street lights')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    test_calculate_min_cut(args.width, args.height, args.num_nodes, args.num_street_lights, args.tx_range, MAX_DISTANCE, args.verbose)


