from message import Message

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

    return routes

def rpl_operation_second_approach(street_lights, origin_node, verbose):
    # Crear una lista de todas las street lights salvo origin_node
    destination = [sl.id for sl in street_lights if sl.id != origin_node.id]

    # Enviar un solo mensaje a la raíz
    message = Message(origin_node.id, destination, "RPL Second Approach: Movement Alert!")
    origin_node.send_message_upwards(message, verbose)
    return message

def rpl_projected_routes(street_lights, origin_node):
    routes = []

    for street_light in street_lights:
        if street_light != origin_node:
            route = origin_node.send_message_through_track(street_light.id)
            routes.append(route)

    return routes

def rpl_multicast(origin_node, verbose):
    message = origin_node.send_movement_alert(verbose)
    return message