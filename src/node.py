import random
from message import Message
from constants import RANK_FACTOR, STRETCH_OF_RANK, MIN_HOP_RANK_INCREASE

class Node:
    def __init__(self, env, id, x, y, tx_range, verbose=False):
        self.env = env
        self.id = id

        self.tx_range = tx_range  # Transmission range to find neighbors
        self.x = x
        self.y = y

        self.neighbors = []
        self.children = [] 

        ## PARA ENVIO DE MENSAJES

        self.is_root = False  # Indica si soy la raíz del DODAG
        self.parent = None  # Padre en el DODAG (nodo hacia el cual reenviar mensajes)
        # self.dodag_id = None  # ID del DODAG
        self.rank = None
        self.preferred_parent = None

        # RPL MULTICAST
        self.mpl_domain_1 = None  # MPL Domain al que pertenece el nodo
        self.mpl_domain_2 = None
        self.received_messages = []  # Lista de mensajes recibidos
        self.senders = []

        env.process(self.run(verbose))

    def run(self, verbose):
        while True:
            yield self.env.timeout(random.uniform(1, 3))
            # if self.rank:
            #     self.send_dio(verbose)

    def send_dio(self, verbose, etx=None):
        for neighbor in self.neighbors:
            neighbor.receive_dio(self, verbose, etx)

    def receive_dio(self, parent, verbose, etx=None):
        step_of_rank = calculate_step_of_rank(etx)
        rank_increase = (RANK_FACTOR + step_of_rank + STRETCH_OF_RANK) * MIN_HOP_RANK_INCREASE
        new_rank = parent.rank + rank_increase
        if not self.rank or self.rank > new_rank:
            self.rank = new_rank
            self.update_preferred_parent(parent, verbose) 
            if verbose: print(f"Node {self.id} received DIO, setting rank to {self.rank}")
            self.send_dio(verbose, etx)

    ## PARA ENVIO DE MENSAJES

    def set_as_root(self, verbose, etx=None, dio=False):
        print("ETX 3: ", etx)
        self.is_root = True
        self.rank = 256
        if verbose: print(f"Node {self.id} is the DODAG Root\n")
        if dio: self.send_dio(verbose, etx)

    def is_dodag_root(self):
        return self.is_root
    
    def is_child_node(self, id):
        # Verifica si el ID proporcionado pertenece a algún hijo
        return any(child.id == id for child in self.children)
    
    def set_preferred_parent(self, parent):
        self.preferred_parent = parent

    def update_preferred_parent(self, parent, verbose):
        if self.preferred_parent:
            self.preferred_parent.children.remove(self)
        self.preferred_parent = parent
        parent.children.append(self)
        if verbose:
            print(f"Node {self.id} updated preferred parent to Node {parent.id}")
        
    def send_message_upwards(self, message, verbose, hops_to_root=0):
        message.add_node_to_route(self)
        if self.id == message.get_destination():
            message.hops_to_root = hops_to_root
            # if verbose: print(f"Node {self.id}: Message delivered to destination {message.get_destination()} :)")
        else:
            # Enviar mensaje hacia arriba en el DODAG (hacia el preferred parent)
            if self.is_root:
                # Soy la raíz, proceso el mensaje aquí o lo reenvío hacia abajo
                message.remove_node_from_route()
                message.hops_to_root = hops_to_root
                if message.is_rpl_second_approach_message():
                    message.add_node_to_route(self)
                    self.forward_message_to_all(message, verbose)
                else:
                    self.send_message_downwards(message, verbose, 0)
            elif self.preferred_parent:
                # if verbose: print(f"Node {self.id}: Message delivered to parent {self.preferred_parent}")

                if message.is_rpl_second_approach_message():
                    message.remove_node_if_is_a_destination(self.id)
                    if message.are_still_destinations():
                        self.preferred_parent.send_message_upwards(message, verbose, hops_to_root + 1) 
                else:
                    self.preferred_parent.send_message_upwards(message, verbose, hops_to_root + 1)
            else:
                if verbose: print(f"Node {self.id}: No preferred parent set to send message upwards.")
    
    def send_message_downwards(self, message, verbose, hops_from_root=0):
        message.add_node_to_route(self)
        if self.id == message.get_destination():
            message.hops_from_root = hops_from_root
            # if verbose: print(f"Node {self.id}: Message delivered to destination {message.get_destination()}")
        else:
            # Enviar mensaje hacia abajo en el DODAG (hacia el destino final)
            shortest_path = self.compute_shortest_path_to_destination(message.get_destination())
            next_hop = shortest_path[1] if len(shortest_path) > 1 else None
            if next_hop is not None:
                # if verbose: print(f"Node {self.id}: Message delivered to: {next_hop}")
                next_hop.send_message_downwards(message, verbose, hops_from_root + 1)
            else:
                if verbose: print(f"Node {self.id}: No route found to destination {message.get_destination()}")
    
    def compute_shortest_path_to_destination(self, destination):
        visited = set()
        queue = [[self]]
        
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node.id == destination:
                return path
            if node.id not in visited:
                for child in node.children:
                    new_path = list(path)
                    new_path.append(child)
                    queue.append(new_path)
                    visited.add(node.id)
        
        return []
    
    def forward_message_to_all(self, message, verbose):
        # tengo que mandar a todas las street lights
        routes = []
        street_lights = message.get_destination()

        # Caso en que la street_light destination sea hijo directo: no hace falta ir a la raiz
        remaining_destinations = []
        for street_light in street_lights:
            is_remaining_destination = True
            for child in self.children:
                if child.id == street_light:
                    # Si el destino es un hijo directo
                    routes.append([self.id, street_light])
                    is_remaining_destination = False
            if is_remaining_destination:
                # Agregar a los destinos restantes que deben enviarse a través de la raíz
                remaining_destinations.append(street_light)

        for street_light in remaining_destinations:
            new_message = Message(self.id, street_light, message.data)
            self.send_message_downwards(new_message, verbose)
            routes.append(new_message.get_route())
        message.add_routes_to_message([message.get_route()] + routes)

    def get_id(self):
        return self.id

    # RPL MULTICAST

    def get_mpl_domain(self):
        return [self.mpl_domain_1, self.mpl_domain_2]
    
    def add_mpl_domain(self, mpl_domain):
        if not self.mpl_domain_1:
            self.mpl_domain_1 = mpl_domain
        else:
            self.mpl_domain_2 = mpl_domain

    def add_sender(self, sender_id):
        self.senders.append(sender_id)

    def receive_message(self, message, domain_address, verbose):
        if message not in self.received_messages:
            self.received_messages.append(message)
            # if verbose: print(f"Node {self.id} received message from {message.get_origin()}")
            message.change_origin(self.id)
            self.forward_message(message, domain_address, verbose)
        # else:
            # if verbose: print(f"Node {self.id} already received message to {message.get_destination()}")

    def forward_message(self, message, domain_address, verbose):
        for neighbor in self.neighbors:
            if message.get_destination() in neighbor.get_mpl_domain() and neighbor != message.get_origin():
                if (self.id == message.get_origin() and message.is_destination_in_multicast_origin_sent_destination(neighbor.get_id())) or (neighbor.get_id() == message.get_last_hop()) or (neighbor.get_id() in self.senders):
                    continue
                else:
                    message.add_destination_to_multicast_origin_sent_destination(neighbor.get_id())
                    self.mpl_domain.increase_message_count()
                    message_id = self.mpl_domain.get_message_count()
                    message.add_node_to_multicast_route(message_id, self.id)
                    message.add_node_to_multicast_route(message_id, neighbor.id)
                    message.change_last_hop(self.id)
                    neighbor.add_sender(self.id)
                    neighbor.receive_message(message, domain_address, verbose)


    # PRINTING AND DEBUGGING

    def print_node_details(self):
        print(f"Node ID: {self.id}")
        print(f"Transmission Range: {self.tx_range}")
        print(f"Is Root: {self.is_root}")
        print(f"Neighbors: {[neighbor.id for neighbor in self.neighbors]}")
        print(f"Children: {[children.id for children in self.children]}")
        print(f"Parent: {self.parent.id if self.parent else None}")
        print(f"Preferred parent: {self.preferred_parent.id if self.preferred_parent else None}")
        print(f"Rank: {self.rank}")
        print(f"MPL Domain 1: {self.mpl_domain_1}")
        print(f"MPL Domain 2: {self.mpl_domain_2}")
        print(f"Received Messages: {[(msg.get_origin(), msg.get_destination()) for msg in self.received_messages]}")
        print()

    def __str__(self):
        return f"Node {self.id}"
    

def calculate_step_of_rank(etx):
    return 100/etx