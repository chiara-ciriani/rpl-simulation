class Message:
    def __init__(self, origin, destination, data):
        self.origin = origin
        self.destination = destination
        self.data = data
        self.route = []  # Lista para almacenar la ruta del mensaje

    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination
    
    def add_node_to_route(self, node):
        self.route.append(node)
    
    def get_route(self):
        print(f"Route: {[node.id for node in self.route]}")
    
    def __eq__(self, other):
        return self.origin == other.origin and self.destination == other.destination and self.data == other.data

    def __hash__(self):
        return hash((self.origin, self.destination, self.data))