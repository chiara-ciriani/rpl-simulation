import random
from message import Message

class Node:
    def __init__(self, env, id, tx_range, verbose=False):
        self.env = env
        self.id = id
        self.tx_range = tx_range  # Transmission range to find neighbors

        self.neighbors = []
        self.children = [] 

        ## PARA ENVIO DE MENSAJES

        self.is_root = False  # Indica si soy la raíz del DODAG
        self.parent = None  # Padre en el DODAG (nodo hacia el cual reenviar mensajes)
        # self.dodag_id = None  # ID del DODAG
        self.rank = None
        self.preferred_parent = None

        # RPL MULTICAST
        self.mpl_domain = None  # MPL Domain al que pertenece el nodo
        self.received_messages = []  # Lista de mensajes recibidos

        env.process(self.run(verbose))

    def run(self, verbose):
        while True:
            yield self.env.timeout(random.uniform(1, 3))
            if self.rank:
                self.send_dio(verbose)

    def send_dio(self, verbose):
        for neighbor in self.neighbors:
            if not neighbor.rank or neighbor.rank > self.rank:
                neighbor.rank = self.rank + 1
                neighbor.parent = self  # Establecer el padre del vecino como el nodo actual (self)
                neighbor.update_preferred_parent(self, verbose)
                if verbose: print(f"Node {self.id} sent DIO to Node {neighbor.id}, setting rank to {self.rank + 1}")
                neighbor.receive_dio(self.rank + 1, verbose)

    def receive_dio(self, rank, verbose):
        if not self.rank or rank < self.rank:
            self.rank = rank
            self.update_preferred_parent(self, verbose)
            if verbose: print(f"Node {self.id} received DIO, setting rank to {self.rank}")
            self.send_dio()

    
    ## PARA ENVIO DE MENSAJES

    def set_as_root(self, verbose):
        self.is_root = True
        self.rank = 0
        # self.dodag_id = self.id  # Se utiliza la ID del nodo como ID del DODAG
        if verbose: print(f"Node {self.id} is the DODAG Root\n")
        self.send_dio(verbose)

    def is_dodag_root(self):
        return self.is_root
    
    def is_child_node(self, id):
        # Verifica si el ID proporcionado pertenece a algún hijo
        return any(child.id == id for child in self.children)
    
    def set_preferred_parent(self, parent):
        self.preferred_parent = parent

    def update_preferred_parent(self, parent, verbose):
        if self.preferred_parent is None or parent.rank < self.preferred_parent.rank:
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
            if verbose: print(f"Node {self.id}: Message delivered to destination {message.get_destination()} :)")
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
                if verbose: print(f"Node {self.id}: Message delivered to parent {self.preferred_parent}")

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
            if verbose: print(f"Node {self.id}: Message delivered to destination {message.get_destination()}")
        else:
            # Enviar mensaje hacia abajo en el DODAG (hacia el destino final)
            shortest_path = self.compute_shortest_path_to_destination(message.get_destination())
            next_hop = shortest_path[1] if len(shortest_path) > 1 else None
            if next_hop is not None:
                if verbose: print(f"Node {self.id}: Message delivered to: {next_hop}")
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
            for child in self.children:
                if child.id == street_light:
                    # Si el destino es un hijo directo
                    routes.append([self.id, street_light])
            else:
                # Agregar a los destinos restantes que deben enviarse a través de la raíz
                remaining_destinations.append(street_light)

        for street_light in remaining_destinations:
            new_message = Message(self.id, street_light, message.data)
            self.send_message_downwards(new_message, verbose)
            routes.append(new_message.get_route())
        message.add_routes_to_message([message.get_route()] + routes)

    # RPL MULTICAST

    def get_mpl_domain(self):
        return self.mpl_domain
    
    def get_id(self):
        return self.id

    def receive_message(self, message, verbose):
        if message not in self.received_messages:
            self.received_messages.append(message)
            if verbose: print(f"Node {self.id} received message from {message.get_origin()}")
            self.forward_message(message, verbose)
        else:
            if verbose: print(f"Node {self.id} already received message to {message.get_destination()}")

    def forward_message(self, message, verbose):
        for neighbor in self.neighbors:
            if neighbor.get_mpl_domain() == self.mpl_domain and neighbor != message.get_origin():
                if self.id == message.get_origin() and message.is_destination_in_multicast_origin_sent_destination(neighbor.get_id()):
                    continue
                else:
                    message.add_destination_to_multicast_origin_sent_destination(neighbor.get_id())
                    self.mpl_domain.increase_message_count()
                    message_id = self.mpl_domain.get_message_count()
                    message.add_node_to_multicast_route(message_id, self.id)
                    message.add_node_to_multicast_route(message_id, neighbor.id)
                    neighbor.receive_message(message, verbose)


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
        print(f"MPL Domain: {self.mpl_domain.id if self.mpl_domain else None}")
        print(f"Received Messages: {[(msg.get_origin(), msg.get_destination()) for msg in self.received_messages]}")
        print()

    def __str__(self):
        return f"Node {self.id}"