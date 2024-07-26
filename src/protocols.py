from message import Message
from utils import find_shortest_paths

def calculate_total_hops(routes):
    return sum(len(route) - 1 for route in routes)

def rpl_operation(street_lights, origin_node, verbose):
    routes = []
    total_hops = 0
    hops_to_root = 0
    hops_from_root = 0

    for street_light in street_lights:
        if street_light != origin_node:
            message = Message(origin_node.id, street_light.get_id(), "RPL Message")
            if origin_node.is_child_node(street_light.get_id()):
                message.add_node_to_route(origin_node)
                message.add_node_to_route(street_light)
                message.hops_to_root = 0
                message.hops_from_root = 1
            else:
                origin_node.send_message_upwards(message, verbose)
            routes.append(message.get_route())
            total_hops += len(message.get_route()) - 1
            hops_to_root += message.hops_to_root
            hops_from_root += message.hops_from_root

    if verbose:
        print()
        print(f"Routes: {[[node.id for node in route] for route in routes]}")

    return total_hops, hops_to_root, hops_from_root

def rpl_operation_second_approach(street_lights, origin_node, verbose):
    # Crear una lista de todas las street lights salvo origin_node
    destinations = [sl.id for sl in street_lights if sl.id != origin_node.id]

    routes = []

    for destination in destinations:
        if origin_node.is_child_node(destination):
            routes.append([origin_node.get_id(), destination])
            destinations.remove(destination)

    # Enviar un solo mensaje a la raíz
    routes_from_operation = []
    if destinations:
        message = Message(origin_node.id, destinations, "RPL Second Approach: Movement Alert!")
        origin_node.send_message_upwards(message, verbose)
        routes_from_operation = message.get_route()

    final_routes = routes + routes_from_operation

    if verbose:
        print()
        if isinstance(final_routes, list) and all(isinstance(route, list) for route in final_routes):
            print(f"Routes: {[[node.id if hasattr(node, 'id') else node for node in route] for route in final_routes]}")
        else:
            print(f"Routes: {[node.id for node in final_routes]}")

    if isinstance(final_routes, list) and all(isinstance(route, list) for route in final_routes):
        total_hops_to_root = len(final_routes[0]) - 1
        hops_from_root = sum(len(route) - 1 for route in final_routes[1:])
    else: 
        total_hops_to_root = len(final_routes)
        hops_from_root = 0

    if isinstance(final_routes, list) and all(isinstance(route, list) for route in final_routes):
        return calculate_total_hops(final_routes), total_hops_to_root, hops_from_root
    return len(final_routes) - 1, total_hops_to_root, hops_from_root

def rpl_projected_routes(street_lights, origin_node, verbose, track1=True):
    routes = []

    for street_light in street_lights:
        if street_light != origin_node:
            if track1:
                route = origin_node.send_message_through_track(street_light.id)
            else:
                route = origin_node.send_message_through_track2(street_light.id)
            if route:
                routes.extend(route)

    if verbose:
        print()
        print(f"Routes: {[[node.id for node in route] for route in routes]}")

    return calculate_total_hops(routes)

def rpl_multicast(origin_node, domain_address, verbose):
    message = origin_node.send_movement_alert(domain_address, verbose)

    routes = message.get_multicast_route()

    if verbose:
        print()
        print(f"Routes: {routes}")

    # total_message_sent = calculate_total_hops(routes)

    # destinations = [node for node in street_lights if node != origin_node]
    # shortest_paths = find_shortest_paths(routes, origin_node, destinations)

    return len(routes)