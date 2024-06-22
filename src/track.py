class Track:
    def __init__(self, ingress, targets):
        self.ingress = ingress
        self.targets = targets
        self.routes = {}           # key: target, value: route (list of nodes)

    def install_route_to_target(self, target, route):
        self.routes[target] = route

    def send_message_through_track(self, target):
        return self.routes[target]
    
    def __str__(self):
        track_info = f"Track Ingress: {self.ingress}\n"
        for target, route in self.routes.items():
            route_ids = [node.id for node in route]
            track_info += f"  Target: {target} - Route: {route_ids}\n"
        return track_info
