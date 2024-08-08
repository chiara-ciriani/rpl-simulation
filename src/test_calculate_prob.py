from calculate_prob_bf import brute_force_solution
from calculate_prob_mc import monte_carlo_simulation

NUM_SIMULATIONS = 1000

# Ejemplo de uso
class Node:
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.link_quality = {}

    def add_neighbor(self, neighbor, link_quality):
        self.neighbors.append(neighbor)
        self.link_quality[neighbor] = link_quality

    def get_link_quality(self, neighbor):
        return self.link_quality.get(neighbor.id, 1.0)

def test_calculate_probability_basic():
    # Test case 1
    nodes = [Node(i) for i in range(1, 5)]
    nodes[0].add_neighbor(nodes[1], 0.9)
    nodes[1].add_neighbor(nodes[0], 0.9)
    nodes[1].add_neighbor(nodes[2], 0.8)
    nodes[2].add_neighbor(nodes[1], 0.8)
    nodes[2].add_neighbor(nodes[3], 0.7)
    nodes[3].add_neighbor(nodes[2], 0.7)

    source_id = 1
    destination_id = 4

    probability_bf = brute_force_solution(nodes, source_id, destination_id)
    assert abs(probability_bf - 0.504) < 1e-6, f'Expected 0.504 but got {probability_bf}'

    probability_mc = monte_carlo_simulation(nodes, source_id, destination_id, NUM_SIMULATIONS)
    assert abs(probability_mc - 0.504) < 1e-1, f'Expected 0.504 but got {probability_mc}'

    print(f'[TEST 1] Brute Force: {probability_bf}')
    print(f'[TEST 1] Monte Carlo: {probability_mc}\n')

    # Test case 2
    nodes = [Node(i) for i in range(1, 4)]
    nodes[0].add_neighbor(nodes[1], 0.5)
    nodes[1].add_neighbor(nodes[2], 0.5)

    source_id = 1
    destination_id = 3

    probability_bf =  brute_force_solution(nodes, source_id, destination_id)
    assert abs(probability_bf- 0.25) < 1e-6, f'Expected 0.25 but got {probability_bf}'

    probability_mc =  monte_carlo_simulation(nodes, source_id, destination_id, NUM_SIMULATIONS)
    assert abs(probability_mc - 0.25) < 1e-1, f'Expected 0.25 but got {probability_mc}'

    print(f'[TEST 2] Brute Force: {probability_bf}')
    print(f'[TEST 2] Monte Carlo: {probability_mc}\n')

    # Test case 3 (there is no possible path)
    nodes = [Node(i) for i in range(1, 4)]
    nodes[0].add_neighbor(nodes[1], 0.5)

    source_id = 1
    destination_id = 3

    probability_bf =  brute_force_solution(nodes, source_id, destination_id)
    assert abs(probability_bf - 0.0) < 1e-6, f'Expected 0.0 but got {probability_bf}'

    probability_mc =  monte_carlo_simulation(nodes, source_id, destination_id, NUM_SIMULATIONS)
    assert abs(probability_mc - 0.0) < 1e-1, f'Expected 0.0 but got {probability_mc}'

    print(f'[TEST 3] Brute Force: {probability_bf}')
    print(f'[TEST 3] Monte Carlo: {probability_mc}\n')

    print("[BASIC TEST] All test cases passed!\n")


def test_calculate_probability_big_domain():
    # Test case 1
    nodes = [Node(i) for i in range(1, 12)]
    nodes[0].add_neighbor(nodes[1], 0.71)
    nodes[1].add_neighbor(nodes[3], 0.85)
    nodes[0].add_neighbor(nodes[2], 0.68)
    nodes[1].add_neighbor(nodes[10], 0.82)
    nodes[2].add_neighbor(nodes[3], 0.82)
    nodes[10].add_neighbor(nodes[4], 0.91)
    nodes[3].add_neighbor(nodes[4], 0.94)
    nodes[3].add_neighbor(nodes[5], 0.83)
    nodes[4].add_neighbor(nodes[6], 0.82)
    nodes[5].add_neighbor(nodes[6], 0.67)
    nodes[6].add_neighbor(nodes[7], 0.76)
    nodes[6].add_neighbor(nodes[8], 0.55)
    nodes[7].add_neighbor(nodes[9], 0.82)
    nodes[8].add_neighbor(nodes[9], 0.91)

    source_id = 1
    destination_id = 10
    probability_bf =  brute_force_solution(nodes, source_id, destination_id)
    assert abs(probability_bf - 0.6379630114287091) < 1e-6, f'Expected 0.6379630114287091 but got {probability_bf}'

    probability_mc =  monte_carlo_simulation(nodes, source_id, destination_id, NUM_SIMULATIONS)
    assert abs(probability_mc - 0.6379630114287091) < 1e-1, f'Expected 0.6379630114287091 but got {probability_mc}'

    print(f'[TEST 1] Brute Force: {probability_bf}')
    print(f'[TEST 1] Monte Carlo: {probability_mc}\n')

    print("[BIGGER DOMAIN TEST] All test cases passed!\n")


if __name__ == "__main__":
    test_calculate_probability_basic()
    test_calculate_probability_big_domain()