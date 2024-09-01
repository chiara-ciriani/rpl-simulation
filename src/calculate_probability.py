import networkx as nx

def build_dependency_graph(G, source_id, destination_id):
    dependency_graph = nx.DiGraph()
    for node in G.nodes:
        for neighbor in G.successors(node):
            dependency_graph.add_edge(node, neighbor)
    return dependency_graph

def calculate_path_probabilities(dependency_graph, source_id, destination_id):
        probabilities = {}
        probabilities[source_id] = 1.0
        
        nodes = list(nx.topological_sort(dependency_graph))
        for node in nodes:
            if node == source_id:
                continue
            incoming_edges = dependency_graph.in_edges(node)
            failure_prob = 1.0
            for edge in incoming_edges:
                parent = edge[0]
                link_quality = G[parent][node]['weight']
                parent_prob = probabilities[parent]
                failure_prob *= (1 - parent_prob * link_quality)
            probabilities[node] = 1 - failure_prob
        
        return probabilities[destination_id]

def calculate_probabilities(nodes, source_id, destination_id):
    G = nx.DiGraph()
    
    for node in nodes:
        for neighbor in node.neighbors:
            link_quality = node.get_link_quality(neighbor)
            G.add_edge(node.id, neighbor.id, weight=1 / link_quality)

    dependency_graph = build_dependency_graph(G, source_id, destination_id)
    probability = calculate_path_probabilities(dependency_graph, source_id, destination_id)
    
    return probability



# BRUTE FORCE


def all_paths_dfs(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in set(graph[vertex].keys()) - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

def calculate_brute_force_probability(nodes, source_id, destination_id):
    G = nx.DiGraph()
    
    for node in nodes:
         for neighbor in node.neighbors:
            link_quality = node.get_link_quality(neighbor)
            G.add_edge(node.id, neighbor.id, weight=1 / link_quality)

    all_paths = list(all_paths_dfs(G, source_id, destination_id))
    
    total_prob = 0
    for path in all_paths:
        path_prob = 1
        for i in range(len(path) - 1):
            path_prob *= G[path[i]][path[i + 1]]['weight']
        total_prob += path_prob
    
    return total_prob



# SIMULATION BIDIRECTIONAL

def build_bidirectional_graph(nodes):
    G = nx.DiGraph()
    
    for node in nodes:
        for neighbor in node.neighbors:
            link_quality = node.get_link_quality(neighbor)
            G.add_edge(node.id, neighbor.id, weight=1 / link_quality)
            G.add_edge(neighbor.id, node.id, weight=1 / neighbor.get_link_quality(node))
    
    return G

def simulate_message_propagation(G, source_id, destination_id, iterations=1000):
    total_successes = 0

    for _ in range(iterations):
        visited = set()
        queue = [(source_id, 1.0)]
        
        while queue:
            current_node, current_prob = queue.pop(0)
            
            # If the message reaches the destination node
            if current_node == destination_id:
                total_successes += current_prob
                break
            
            visited.add(current_node)
            
            for neighbor in G.successors(current_node):
                if neighbor not in visited:
                    link_prob = 1 / G[current_node][neighbor]['weight']
                    queue.append((neighbor, current_prob * link_prob))
                    visited.add(neighbor)
    
    return total_successes / iterations

def calculate_probabilities_multicast(nodes, source_id, destination_id, iterations=1000):
    G = build_bidirectional_graph(nodes)
    probability = simulate_message_propagation(G, source_id, destination_id, iterations)
    return probability