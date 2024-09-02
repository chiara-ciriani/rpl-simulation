class Message:
    def __init__(self, origin, destination, data):
        self.origin = origin
        self.destination = destination
        self.data = data
        self.route = []  # List to store the message route
        self.multicast_route = []  # List of tuples to store the multicast route
        self.multicast_origin_sent_destination = []
        self.hops_to_root = 0
        self.hops_from_root = 0
        self.last_hop = None

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

    def add_node_to_multicast_route(self, node1, node2):
        pair = tuple(sorted([node1, node2]))
        if pair not in self.multicast_route:
            self.multicast_route.append(pair)

    def get_multicast_route(self):
        unique_routes_set = set(self.multicast_route)
        unique_routes_array = [list(pair) for pair in unique_routes_set]
        return unique_routes_array
    
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
    
    def get_last_hop(self):
        return self.last_hop
    
    def change_last_hop(self, new_last_hop):
        self.last_hop = new_last_hop

    def change_origin(self, new_origin):
        self.origin = new_origin

    def __eq__(self, other):
        return self.origin == other.origin and self.destination == other.destination and self.data == other.data

    def __hash__(self):
        return hash((self.origin, self.destination, self.data))