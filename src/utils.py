from heapq import heappop, heappush

from graph import Graph

def minimum_path_dijkstra(graph, origin):
    distance = {}
    parent = {}
    for v in graph.obtener_vertices():
        distance[v] = float("inf")
    distance[origin.id] = 0
    parent[origin.id] = None
    heap = []
    heappush(heap, (0, origin.id))
    while len(heap):
        _, v = heappop(heap)
        for w in graph.adyacentes(v):
            if distance[v] + graph.peso_arista(v, w) < distance[w]:
                distance[w] = distance[v] + graph.peso_arista(v, w)
                parent[w] = v
                heappush(heap, (distance[w], w))
    return parent, distance

def reconstruct_path(parents, destination):
    path = []

    if destination not in parents:
        return path

    while destination is not None:
        path.append(destination)
        destination = parents[destination]

    return path[::-1]

def find_shortest_paths(routes, start_node, destinations):
    graph = Graph(es_dirigido=False, es_pesado=True)
    
    # Construir el grafo
    vertices = set()
    for route in routes:
        u, v = route
        vertices.add(u)
        vertices.add(v)
    for vertice in vertices:
        graph.agregar_vertice(vertice)
    for route in routes:
        u, v = route
        graph.agregar_arista(u, v, peso=1)
    
    # Ejecutar Dijkstra desde el nodo de inicio
    parents, _ = minimum_path_dijkstra(graph, start_node)
    
    # Construir los caminos más cortos para cada destino
    shortest_path = []
    for destination in destinations:
        path = reconstruct_path(parents, destination.id)
        shortest_path.append(path)
    
    return shortest_path