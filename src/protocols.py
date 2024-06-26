from message import Message
from utils import find_shortest_paths

def calculate_total_hops(routes):
    return sum(len(route) - 1 for route in routes)

def rpl_operation(street_lights, origin_node, verbose):
    routes = []

    for street_light in street_lights:
        if street_light != origin_node:
            message = Message(origin_node.id, street_light.id, "RPL Message")
            if origin_node.is_child_node(street_light.id):
                message.add_node_to_route(origin_node)
                message.add_node_to_route(street_light)
            else:
                origin_node.send_message_upwards(message, verbose)
            routes.append(message.get_route())

    if verbose:
        print()
        print(f"Routes: {[[node.id for node in route] for route in routes]}")

    return calculate_total_hops(routes)

def rpl_operation_second_approach(street_lights, origin_node, verbose):
    # Crear una lista de todas las street lights salvo origin_node
    destination = [sl.id for sl in street_lights if sl.id != origin_node.id]

    # Enviar un solo mensaje a la raíz
    message = Message(origin_node.id, destination, "RPL Second Approach: Movement Alert!")
    origin_node.send_message_upwards(message, verbose)

    routes = message.get_route()

    if verbose:
        print()
        print(f"Routes: {[[node.id if hasattr(node, 'id') else node for node in route] for route in routes]}")

    if isinstance(routes, list) and all(isinstance(route, list) for route in routes):
        return calculate_total_hops(routes)
    return len(routes) - 1

def rpl_projected_routes(street_lights, origin_node, verbose):
    routes = []

    for street_light in street_lights:
        if street_light != origin_node:
            route = origin_node.send_message_through_track(street_light.id)
            routes.append(route)

    if verbose:
        print()
        print(f"Routes: {[[node.id for node in route] for route in routes]}")

    return calculate_total_hops(routes)

def rpl_multicast(origin_node, street_lights, verbose):
    message = origin_node.send_movement_alert(verbose)

    routes = message.get_multicast_route()

    if verbose:
        print()
        print(f"Routes: {routes}")

    # total_message_sent = calculate_total_hops(routes)

    destinations = [node for node in street_lights if node != origin_node]
    shortest_paths = find_shortest_paths(routes, origin_node, destinations)

    return calculate_total_hops(shortest_paths)