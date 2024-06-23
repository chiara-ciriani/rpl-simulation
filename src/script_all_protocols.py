import subprocess
import argparse

def run_simulations(num_simulations, tx_range, num_nodes, num_street_lights, verbose):
    # Listas para almacenar los resultados
    rpl_operation_results = []
    rpl_operation_second_approach_results = []
    rpl_projected_routes_results = []
    rpl_multicast_results = []

    for _ in range(num_simulations):
        result = subprocess.run(
            ['python', 'all_protocols.py',
             '--tx_range', str(tx_range),
             '--num_nodes', str(num_nodes),
             '--num_street_lights', str(num_street_lights)],
            capture_output=True,
            text=True
        )

        # Capturar la salida del script para analizar los resultados
        output_lines = result.stdout.splitlines()

        # Obtener los resultados de los protocolos
        rpl_operation_total_hops = int(output_lines[0].split(': ')[-1])
        rpl_operation_second_approach_total_hops = int(output_lines[1].split(': ')[-1])
        rpl_projected_routes_total_hops = int(output_lines[2].split(': ')[-1])
        rpl_multicast_total_hops = int(output_lines[3].split(': ')[-1])

        # Almacenar los resultados en las listas
        rpl_operation_results.append(rpl_operation_total_hops)
        rpl_operation_second_approach_results.append(rpl_operation_second_approach_total_hops)
        rpl_projected_routes_results.append(rpl_projected_routes_total_hops)
        rpl_multicast_results.append(rpl_multicast_total_hops)

    # Imprimir los resultados promedio o realizar el análisis deseado
    print(f"Average hops for RPL Operation: {sum(rpl_operation_results) / num_simulations}")
    print(f"Average hops for RPL Operation Second Approach: {sum(rpl_operation_second_approach_results) / num_simulations}")
    print(f"Average hops for RPL Projected Routes: {sum(rpl_projected_routes_results) / num_simulations}")
    print(f"Average hops for RPL Multicast: {sum(rpl_multicast_results) / num_simulations}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run multiple simulations of all protocols with different parameters.")
    parser.add_argument('--num_simulations', type=int, default=100, help='Number of simulations to run')
    parser.add_argument('--tx_range', type=int, default=30, help='Transmission range for each node')
    parser.add_argument('--num_nodes', type=int, default=10, help='Total number of nodes in the network')
    parser.add_argument('--num_street_lights', type=int, default=3, help='Number of street lights')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    run_simulations(args.num_simulations, args.tx_range, args.num_nodes, args.num_street_lights, args.verbose)
