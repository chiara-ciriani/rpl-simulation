import random
import simpy
from plot_table import print_comparison_table
from plot_results import plot_results

from protocols import rpl_multicast, rpl_operation, rpl_operation_second_approach, rpl_projected_routes
from network import create_network_with_spanning_tree, plot_network
from street_light import StreetLight

def send_to_all_street_lights_using_all_protocols(tx_range, num_nodes, num_street_lights, verbose=False):
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

    rpl_operation_total_hops, rpl_operation_hops_to_root, rpl_operation_hops_from_root = rpl_operation(street_lights, origin_node, verbose)
    rpl_operation_second_approach_total_hops, rpl_operation_second_approach_hops_to_root, rpl_operation_second_approach_hops_from_root = rpl_operation_second_approach(street_lights, origin_node, verbose)
    rpl_projected_routes_total_hops = rpl_projected_routes(street_lights, origin_node, verbose)
    rpl_multicast_total_hops = rpl_multicast(origin_node, street_lights, verbose)

    # Plot the resulting DODAG
    if verbose:
        plot_network(nodes, positions)

    return rpl_operation_total_hops, rpl_operation_hops_to_root, rpl_operation_hops_from_root, rpl_operation_second_approach_total_hops, rpl_operation_second_approach_hops_to_root, rpl_operation_second_approach_hops_from_root, rpl_projected_routes_total_hops, rpl_multicast_total_hops

def run_simulations(num_simulations, tx_range, num_nodes, num_street_lights, verbose):
    # Listas para almacenar los resultados
    rpl_operation_results = []
    rpl_operation_second_approach_results = []
    rpl_projected_routes_results = []
    rpl_multicast_results = []

    for _ in range(num_simulations):
        rpl_operation_total_hops, rpl_operation_hops_to_root, rpl_operation_hops_from_root, rpl_operation_second_approach_total_hops, rpl_operation_second_approach_hops_to_root, rpl_operation_second_approach_hops_from_root, rpl_projected_routes_total_hops, rpl_multicast_total_hops = send_to_all_street_lights_using_all_protocols(tx_range, num_nodes, num_street_lights, verbose)

        # Almacenar los resultados en las listas
        rpl_operation_results.append([rpl_operation_total_hops, rpl_operation_hops_to_root, rpl_operation_hops_from_root])
        rpl_operation_second_approach_results.append([rpl_operation_second_approach_total_hops, rpl_operation_second_approach_hops_to_root, rpl_operation_second_approach_hops_from_root])
        rpl_projected_routes_results.append(rpl_projected_routes_total_hops)
        rpl_multicast_results.append(rpl_multicast_total_hops)

    # Calcular los promedios
    rpl_operation_averages = [sum(x) / num_simulations for x in zip(*rpl_operation_results)]
    rpl_operation_second_approach_averages = [sum(x) / num_simulations for x in zip(*rpl_operation_second_approach_results)]
    rpl_projected_routes_average = sum(rpl_projected_routes_results) / num_simulations
    proposed_solution_average = sum(rpl_multicast_results) / num_simulations

    # Imprimir los resultados promedio o realizar el análisis deseado
    if verbose:
        print(f"Number of simulations:  {num_simulations}\n")

        print(f"Number of nodes:  {num_nodes}\n")

        print(f"Number of street lights:  {num_street_lights}\n")

        print(f"Standard RPL Operation:   Average hops  |  Average number of hops from origin to the Root  |  From Root to destination ")
        print(f"Standard RPL Operation: {rpl_operation_averages[0]}, {rpl_operation_averages[1]}, {rpl_operation_averages[2]}\n")

        print(f"Standard RPL Operation alternative:   Average hops  |  Average number of hops from origin to the Root  |  From Root to destination ")
        print(f"Standard RPL Operation alternative: {rpl_operation_second_approach_averages[0]}, {rpl_operation_second_approach_averages[1]}, {rpl_operation_second_approach_averages[2]}\n")

        print(f"RPL Projected Routes:   Average hops")
        print(f"RPL Projected Routes: {rpl_projected_routes_average}\n")

        print(f"Proposed Solution:   Average hops")
        print(f"Proposed Solution: {proposed_solution_average}")

    return rpl_operation_averages[0], rpl_operation_averages[1], rpl_operation_averages[2], rpl_operation_second_approach_averages[0], rpl_operation_second_approach_averages[1], rpl_operation_second_approach_averages[2], rpl_projected_routes_average, proposed_solution_average

def run_simulations_for_different_node_and_light_counts(num_simulations, tx_range, node_and_light_counts, verbose):
    results = {
        'num_nodes': [],
        'num_street_lights': [],
        'rpl_hops': [],
        'rpl_hops_from_origin': [],
        'rpl_hops_from_root': [],
        'rpl_second_approach_hops': [],
        'rpl_second_approach_hops_from_origin': [],
        'rpl_second_approach_hops_from_root': [],
        'projected_routes_hops': [],
        'proposed_solution_hops': []
    }

    for num_nodes, num_street_lights in node_and_light_counts:
        print(f"Running simulations for {num_nodes} nodes and {num_street_lights} street lights...")
        rpl_hops, rpl_hops_from_origin, rpl_hops_from_root, rpl_second_approach_hops, rpl_second_approach_hops_from_origin, rpl_second_approach_hops_from_root, projected_routes_hops, proposed_solution_hops = run_simulations(num_simulations, tx_range, num_nodes, num_street_lights, verbose)
        
        results['num_nodes'].append(num_nodes)
        results['num_street_lights'].append(num_street_lights)
        results['rpl_hops'].append(rpl_hops)
        results['rpl_hops_from_origin'].append(rpl_hops_from_origin)
        results['rpl_hops_from_root'].append(rpl_hops_from_root)
        results['rpl_second_approach_hops'].append(rpl_second_approach_hops)
        results['rpl_second_approach_hops_from_origin'].append(rpl_second_approach_hops_from_origin)
        results['rpl_second_approach_hops_from_root'].append(rpl_second_approach_hops_from_root)
        results['projected_routes_hops'].append(projected_routes_hops)
        results['proposed_solution_hops'].append(proposed_solution_hops)

    return results

NUM_SIMULATIONS = 1000
TX_RANGE = 30 
VERBOSE = False
# NODE_AND_LIGHT_COUNTS = [(100, 5), (200, 10), (400, 20), (600, 30), (800, 40), (1000, 50)]
# NODE_AND_LIGHT_COUNTS = [(10, 2), (20, 2), (30, 2), (40, 2), (50, 2)]
NODE_AND_LIGHT_COUNTS = [(100, 2), (100, 5), (100, 10), (100, 20), (100, 40)]

results = run_simulations_for_different_node_and_light_counts(NUM_SIMULATIONS, TX_RANGE, NODE_AND_LIGHT_COUNTS, VERBOSE)

print_comparison_table(results)

plot_results(results)