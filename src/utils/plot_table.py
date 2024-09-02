def print_comparison_table(results):
    print("Comparison of Average Number of Hops for Different Protocols:")
    print(f"{'Num Nodes':<10} {'Num SL':<10} {'RPL Operation':<15} {'RPL Alt.':<15} {'Projected Routes':<20} {'Proposed Solution':<20}")
    for i in range(len(results['num_nodes'])):
        print(f"{results['num_nodes'][i]:<10} {results['num_street_lights'][i]:<10} {results['rpl_hops'][i]:<15.2f} {results['rpl_second_approach_hops'][i]:<15.2f} {results['projected_routes_hops'][i]:<20.2f} {results['proposed_solution_hops'][i]:<20.2f}")
