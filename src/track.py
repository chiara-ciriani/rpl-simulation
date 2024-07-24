class Track:
    def __init__(self, ingress, targets):
        self.ingress = ingress
        self.targets = targets
        self.routes = {}           # key: target, value: list of routes (each route is a list of nodes)

    def install_route_to_target(self, target, route):
        if target not in self.routes:
            self.routes[target] = []
        self.routes[target].append(route)

    def send_message_through_track(self, target):
        # Return the list of all routes for the given target
        if target in self.routes:
            return self.routes[target]
        else:
            return None

    def __str__(self):
        track_info = f"Track Ingress: {self.ingress}\n"
        for target, routes in self.routes.items():
            for i, route in enumerate(routes):
                route_ids = [node.id for node in route]
                track_info += f"  Target: {target} - Route {i + 1}: {route_ids}\n"
        return track_info
