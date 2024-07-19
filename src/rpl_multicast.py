import argparse
import random
import simpy

from network import create_network_with_spanning_tree, plot_network
from protocols import rpl_multicast
from street_light import StreetLight

def send_message_in_mpl_domain(tx_range, num_nodes, num_street_lights, verbose=False):
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

    total_hops = rpl_multicast(origin_node, street_lights, verbose)
    print(total_hops)
    
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

    send_message_in_mpl_domain(args.tx_range, args.num_nodes, args.num_street_lights, args.verbose)


# FALTA: 
#  maybe mejorar la forma de crear domains
# faltaria mezclar ambas formas y contar en ambas el number of hops
# despues eso se lo podriamos pasar al algoritmo de calculaciones?
# el tema es que no tendriamos los canales y eso, pero podría ser una probabilidad
# TO DO: cambiar canales en el otro codigo a probabilidad maybe
# pasarle al algoritmo el route y la lista de ids de nodes mejor
# FALTA TAMBIEN AGREGAR QUE GUARDE LA ROUTE EN MULTICAST. Pero creo q ahi vamos a tener muchas routes y dps vamos a tener q calcular cada una por separado y sumar

# AGREGAR PROJECTED ROUTES
# elegir street light al azar y mandar mensaje a cada street light por shortest path