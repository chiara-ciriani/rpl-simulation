import argparse
import simpy

from classes.mpl_domain import MPL_Domain
from classes.street_light import StreetLight

from creating_domains_dio import add_nodes_to_multipath_domain, add_nodes_to_multipath_domain_common_neighbors, compute_tracks_multipath, compute_tracks_multipath_disjoint_paths, create_network_with_dio, plot_network, plot_domain_dodag

from common_neighbor.common_neighbor_domains import add_nodes_to_multipath_domain_common_neighbors_range_extended

from protocols import rpl_multicast, rpl_projected_routes

from metrics.probability.calculate_prob_mc import monte_carlo_simulation

from metrics.mincut.calculate_min_cut import calculate_min_cut

STREET_LIGHT_INDEXES = [0, 5, 10]

NUM_SIMULATIONS=1000

def calculate_metrics(width, height, num_nodes, num_street_lights, tx_range, max_distance, direct_comunication, verbose=False):
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
    if direct_comunication:
        add_nodes_to_multipath_domain_common_neighbors(mpl_domain_2, nodes, verbose)
    else:
        add_nodes_to_multipath_domain_common_neighbors_range_extended(mpl_domain_2, nodes, verbose)

    mpl_domain_address_3 = "MPL_Domain_3"
    mpl_domain_3 = MPL_Domain(3, mpl_domain_address_3)
    add_nodes_to_multipath_domain(mpl_domain_3, track_nodes2, verbose)

    # Run the simulation
    env.run(until=30)

    results = {
        'transmissions': {},  # Aquí almacenaremos el número de transmisiones para cada street light
        'probabilities': {},  # Aquí almacenaremos las probabilidades para cada street light
        'min_cuts': {}  # Aquí almacenaremos los min cut para cada dominio
    }

    # Guardar la longitud de cada dominio
    results['domain_lengths'] = {
        'domain1': len(mpl_domain_1.nodes),
        'domain2': len(mpl_domain_2.nodes),
        'domain3': len(mpl_domain_3.nodes)
    }

    # Calcula las probabilidades para cada origen
    for source_id in STREET_LIGHT_INDEXES:
        destination_ids = [light.id for light in street_lights if light.id != source_id]

        probability_mc_domain1, _ = monte_carlo_simulation(mpl_domain_1.get_nodes(), source_id, destination_ids, NUM_SIMULATIONS)
        probability_mc_domain2, _ = monte_carlo_simulation(mpl_domain_2.get_nodes(), source_id, destination_ids, NUM_SIMULATIONS)
        probability_mc_domain3, _ = monte_carlo_simulation(mpl_domain_3.get_nodes(), source_id, destination_ids, NUM_SIMULATIONS)

        results['probabilities'][f'source_{source_id}'] = {
            'domain1': probability_mc_domain1,
            'domain2': probability_mc_domain2,
            'domain3': probability_mc_domain3
        }

    # Calcular el corte mínimo de nodos y aristas para desconectar todo el dominio
    min_vertex_cut_domain1, min_edge_cut_domain1 = calculate_min_cut(mpl_domain_1.get_nodes())
    min_vertex_cut_domain2, min_edge_cut_domain2 = calculate_min_cut(mpl_domain_2.get_nodes())
    min_vertex_cut_domain3, min_edge_cut_domain3 = calculate_min_cut(mpl_domain_3.get_nodes())

    results['min_cuts']['domain1'] = {'vertex_cut': min_vertex_cut_domain1, 'edge_cut': min_edge_cut_domain1}
    results['min_cuts']['domain2'] = {'vertex_cut': min_vertex_cut_domain2, 'edge_cut': min_edge_cut_domain2}
    results['min_cuts']['domain3'] = {'vertex_cut': min_vertex_cut_domain3, 'edge_cut': min_edge_cut_domain3}

    # Almacenar los resultados de las transmisiones para cada street light
    for street_light_idx in STREET_LIGHT_INDEXES:
        street_light = street_lights[street_light_idx]
        origin_node = street_light

        # Realizar simulaciones o cálculos específicos
        total_hops_projected_routes = rpl_projected_routes(street_lights, origin_node, verbose, True)
        total_hops_projected_routes2 = rpl_projected_routes(street_lights, origin_node, verbose, False)
        total_hops_domain1 = rpl_multicast(origin_node, mpl_domain_address_1, verbose)

        # Limpiar los mensajes recibidos para la siguiente simulación
        for node in mpl_domain_1.get_nodes():
            node.received_messages = []
            node.senders = []

        total_hops_domain2 = rpl_multicast(origin_node, mpl_domain_address_2, verbose)

        for node in mpl_domain_2.get_nodes():
            node.received_messages = []
            node.senders = []

        total_hops_domain3 = rpl_multicast(origin_node, mpl_domain_address_3, verbose)

        for node in mpl_domain_3.get_nodes():
            node.received_messages = []
            node.senders = []

        # Almacenar resultados de transmisiones
        results['transmissions'][street_light.get_id()] = {
            'projected_routes1': total_hops_projected_routes,
            'projected_routes2': total_hops_projected_routes2,
            'domain1': total_hops_domain1,
            'domain2': total_hops_domain2,
            'domain3': total_hops_domain3
        }

    if verbose:
        print(f"Edges removed track length: {len(track_nodes)}")
        print(f"Disjoint paths track length: {len(track_nodes2)}")

        print(f"Edges removed domain length: {len(mpl_domain_1.nodes)}")
        print(f"Disjoint paths domain length: {len(mpl_domain_3.nodes)}")
        print(f"Common neighbor domain length: {len(mpl_domain_2.nodes)}\n")

        for source_id in STREET_LIGHT_INDEXES:
            print(f"Projected Routes Edges Removed: {results['transmissions'][source_id]['projected_routes1']}")
            print(f"Projected Routes Disjoint Paths: {results['transmissions'][source_id]['projected_routes2']}")
            print(f"Proposed Solution with Edges Removed Domain: {results['transmissions'][source_id]['domain1']}")
            print(f"Proposed Solution with Disjoint Paths Domain: {results['transmissions'][source_id]['domain3']}")
            print(f"Proposed Solution with Common Neighbor Domain: {results['transmissions'][source_id]['domain2']}\n")

            print(f"Edges Removed Monte Carlo (Source {source_id}): {results['probabilities'][f'source_{source_id}']['domain1']}")
            print(f"Disjoint Paths Monte Carlo (Source {source_id}): {results[f'probabilities'][f'source_{source_id}']['domain3']}")
            print(f"Common Neighbor Monte Carlo (Source {source_id}): {results['probabilities'][f'source_{source_id}']['domain2']}\n")
        
        print(f"Edges Removed Min Vertex Cut: {min_vertex_cut_domain1}")
        print(f"Edges Removed Min Edge Cut: {min_edge_cut_domain1}")

        print(f"Disjoint Paths Min Vertex Cut: {min_vertex_cut_domain3}")
        print(f"Disjoint Paths Min Edge Cut: {min_edge_cut_domain3}")

        print(f"Common Neighbor Min Vertex Cut: {min_vertex_cut_domain2}")
        print(f"Common Neighbor Min Edge Cut: {min_edge_cut_domain2}")

        plot_network(nodes, mpl_domain_1, mpl_domain_2, mpl_domain_3)

        plot_domain_dodag(nodes, mpl_domain_1, "Edges Removed", verbose)
        plot_domain_dodag(nodes, mpl_domain_2, "Common Neighbor", verbose)
        plot_domain_dodag(nodes, mpl_domain_3, "Disjoint Paths", verbose)

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send messages to all street lights in a network simulation.")
    parser.add_argument('--max_distance', type=int, default=200, help='Distance between street lights')
    parser.add_argument('--direct_comunication', action='store_true', help='Only direct communication. Not range extended')
    parser.add_argument('--width', type=int, default=2500, help='Width of the network')
    parser.add_argument('--height', type=int, default=2500, help='Height of the network')
    parser.add_argument('--num_nodes', type=int, default=200, help='Total number of nodes in the network')
    parser.add_argument('--num_street_lights', type=int, default=11, help='Number of street lights')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    if args.direct_comunication:
        tx_range = args.max_distance
    else:
        tx_range = args.max_distance * 2

    calculate_metrics(args.width, args.height, args.num_nodes, args.num_street_lights, args.tx_range, args.max_distance, args.verbose)


