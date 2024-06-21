class Message:
    def __init__(self, origin, destination, data):
        self.origin = origin
        self.destination = destination
        self.data = data
        self.route = []  # Lista para almacenar la ruta del mensaje
        self.multicast_route = {}

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
    
    def __eq__(self, other):
        return self.origin == other.origin and self.destination == other.destination and self.data == other.data

    def __hash__(self):
        return hash((self.origin, self.destination, self.data))