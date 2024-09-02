import matplotlib.pyplot as plt

def plot_results(results):
    plt.figure(figsize=(12, 8))

    plt.plot(results['num_nodes'], results['rpl_hops'], label='RPL Operation')
    plt.plot(results['num_nodes'], results['rpl_second_approach_hops'], label='RPL Operation Alt')
    plt.plot(results['num_nodes'], results['projected_routes_hops'], label='Projected Routes')
    plt.plot(results['num_nodes'], results['proposed_solution_hops'], label='Proposed Solution')

    plt.xlabel('Number of Nodes')
    plt.ylabel('Average Number of Hops')
    plt.title('Comparison of Average Number of Hops for Different Protocols')
    plt.legend()
    plt.grid(True)
    plt.show()