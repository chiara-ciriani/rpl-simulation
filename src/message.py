class Message:
    def __init__(self, origin, destination, data):
        self.origin = origin
        self.destination = destination
        self.data = data
        self.route = []  # Lista para almacenar la ruta del mensaje
        self.multicast_route = {}
        self.multicast_origin_sent_destination = []
        self.hops_to_root = 0
        self.hops_from_root = 0

    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination
    
    def add_node_to_route(self, node):
        self.route.append(node)

    def remove_node_from_route(self):
        self.route.pop()

    def get_route(self):
        return self.route
    
    def print_route(self):
        if all(isinstance(route, list) for route in self.route):
            # Si self.route es una lista de listas
            for route in self.route:
                print(f"Route: {[node.id for node in route]}")
        else:
            # Si self.route es una lista simple
            print(f"Route: {[node.id for node in self.route]}")

    def add_node_to_multicast_route(self, id, node):
        current_route = self.multicast_route.get(id, []) 
        current_route.append(node)
        self.multicast_route[id] = current_route

    def get_multicast_route(self):
        result = []
        for route in self.multicast_route.values():
            result.append(route)
        return result
    
    def add_destination_to_multicast_origin_sent_destination(self, destination_id):
        self.multicast_origin_sent_destination.append(destination_id)

    def is_destination_in_multicast_origin_sent_destination(self, destination_id):
        return destination_id in self.multicast_origin_sent_destination
    
    def is_rpl_second_approach_message(self):
        return self.data == "RPL Second Approach: Movement Alert!"
    
    def add_routes_to_message(self, routes):
        self.route = routes

    def remove_node_if_is_a_destination(self, node_id):
        if node_id in self.destination:
            self.destination.remove(node_id)

    def are_still_destinations(self):
        return len(self.destination)

    def __eq__(self, other):
        return self.origin == other.origin and self.destination == other.destination and self.data == other.data

    def __hash__(self):
        return hash((self.origin, self.destination, self.data))