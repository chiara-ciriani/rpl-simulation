import subprocess
import argparse

def run_simulations(num_simulations, tx_range, num_nodes, num_street_lights, output_file, verbose):
    # Listas para almacenar los resultados
    rpl_operation_results = []
    rpl_operation_second_approach_results = []
    rpl_projected_routes_results = []
    rpl_multicast_results = []

    for _ in range(num_simulations):
        result = subprocess.run(
            ['python', 'test_all_protocols.py',
             '--tx_range', str(tx_range),
             '--num_nodes', str(num_nodes),
             '--num_street_lights', str(num_street_lights)],
            capture_output=True,
            text=True
        )

        # Capturar la salida del script para analizar los resultados
        output_lines = result.stdout.splitlines()

        # Obtener los resultados de los protocolos
        if output_lines:
            rpl_operation_data = output_lines[0].split(': ')[-1].strip('()').split(', ')
            rpl_operation_total_hops = int(rpl_operation_data[0])
            rpl_operation_hops_to_root = int(rpl_operation_data[1])
            rpl_operation_hops_from_root = int(rpl_operation_data[2])

            rpl_operation_second_approach_data = output_lines[1].split(': ')[-1].strip('()').split(', ')
            rpl_operation_second_approach_total_hops = int(rpl_operation_second_approach_data[0])
            rpl_operation_second_approach_hops_to_root = int(rpl_operation_second_approach_data[1])
            rpl_operation_second_approach_hops_from_root = int(rpl_operation_second_approach_data[2])

            rpl_projected_routes_total_hops = int(output_lines[2].split(': ')[-1]) if len(output_lines) > 2 else 0
            rpl_multicast_total_hops = int(output_lines[3].split(': ')[-1]) if len(output_lines) > 3 else 0
        else:
            rpl_operation_total_hops = 0
            rpl_operation_hops_to_root = 0
            rpl_operation_hops_from_root = 0
            rpl_operation_second_approach_total_hops = 0
            rpl_operation_second_approach_hops_to_root = 0
            rpl_operation_second_approach_hops_from_root = 0
            rpl_projected_routes_total_hops = 0
            rpl_multicast_total_hops = 0

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

    # Escribir los resultados en un archivo
    with open(output_file, 'w') as file:
        file.write(f"Number of simulations: {num_simulations}\n\n")

        file.write(f"Number of nodes:  {num_nodes}\n")

        file.write(f"Number of street lights:  {num_street_lights}\n")

        file.write(f"Standard RPL Operation:   Average hops  |  Average number of hops from origin to the Root  |  From Root to destination \n")
        file.write(f"Standard RPL Operation: {rpl_operation_averages[0]}, {rpl_operation_averages[1]}, {rpl_operation_averages[2]}\n\n")

        file.write(f"Standard RPL Operation alternative:   Average hops  |  Average number of hops from origin to the Root  |  From Root to destination \n")
        file.write(f"Standard RPL Operation alternative: {rpl_operation_second_approach_averages[0]}, {rpl_operation_second_approach_averages[1]}, {rpl_operation_second_approach_averages[2]}\n\n")

        file.write(f"RPL Projected Routes:   Average hops\n")
        file.write(f"RPL Projected Routes: {rpl_projected_routes_average}\n\n")

        file.write(f"Proposed Solution:   Average hops\n")
        file.write(f"Proposed Solution: {proposed_solution_average}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run multiple simulations of all protocols with different parameters.")
    parser.add_argument('--num_simulations', type=int, default=100, help='Number of simulations to run')
    parser.add_argument('--tx_range', type=int, default=30, help='Transmission range for each node')
    parser.add_argument('--num_nodes', type=int, default=10, help='Total number of nodes in the network')
    parser.add_argument('--num_street_lights', type=int, default=3, help='Number of street lights')
    parser.add_argument('--output_file', type=str, default='simulation_results.txt', help='Output file to save the results')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()

    run_simulations(args.num_simulations, args.tx_range, args.num_nodes, args.num_street_lights, args.output_file, args.verbose)
