import simpy
import random
from network import create_network_with_mpl_domain, plot_dodag
from street_light import StreetLight

def main():
    env = simpy.Environment()
    tx_range = 30  # Increased transmission range for each node
    num_nodes = 10 # Total number of nodes in the network
    num_street_lights = 3  # Number of street lights

    # Create the network
    nodes, positions = create_network_with_mpl_domain(env, num_nodes, num_street_lights, tx_range)
    street_lights = [node for node in nodes if isinstance(node, StreetLight)]

    # Run the simulation
    env.run(until=30)

    print()

    for node in nodes:
        node.print_node_details()

    print()

    origin_node = random.choice(street_lights)

    print(f"Street light {origin_node.id} detected movement\n")
    origin_node.send_movement_alert()
    
    # Plot the resulting DODAG
    plot_dodag(nodes, positions)


if __name__ == "__main__":
    main()


# FALTA: 
#  maybe mejorar la forma de crear domains
# faltaria mezclar ambas formas y contar en ambas el number of hops
# despues eso se lo podriamos pasar al algoritmo de calculaciones?
# el tema es que no tendriamos los canales y eso, pero podría ser una probabilidad
# TO DO: cambiar canales en el otro codigo a probabilidad maybe
# pasarle al algoritmo el route y la lista de ids de nodes mejor

# AGREGAR PROJECTED ROUTES