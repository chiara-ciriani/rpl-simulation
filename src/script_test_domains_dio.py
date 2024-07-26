import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from test_domains_dio import send_to_all_street_lights
from test_domains_dio_multipath import send_to_all_street_lights_multipath

NUM_STREET_LIGHTS=11

width = 65
height = 60
num_nodes = 200
tx_range = 5 
max_distance = 5 

all_results = []

for _ in range(500):
    # results, root_position = send_to_all_street_lights(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, False)
    results, root_position = send_to_all_street_lights_multipath(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, False)
    all_results.append((results, root_position))

data = []
for results, root_position in all_results:
    for sl_id, values in results.items():
        data.append({
            'StreetLight': sl_id,
            #'RPL': values[0],
            #'Optimized RPL': values[1],
            'Projected Routes - Edges removed': values[0],
            'Projected Routes - Disjoint Paths': values[1],
            #'Proposed Solution': values[3],
            'Proposed Solution - Edges removed': values[2],
            'Proposed Solution - Disjoint paths': values[3],
            'Proposed Solution - Common Neighbor Domain': values[4],
            'RootX': root_position[0],
            'RootY': root_position[1],
            'num_nodes': num_nodes
        })


df = pd.DataFrame(data)
print(df)

# Resumen estadístico
summary = df.describe()
print(summary)

# Agrupar por StreetLight y calcular medias
grouped = df.groupby('StreetLight').mean()
print(grouped)

# Boxplot para comparar resultados de los enfoques por street light
# approaches = ['RPL', 'Optimized RPL', 'Projected Routes', 'Domain 1', 'Domain 2']
# for approach in approaches:
#     plt.figure(figsize=(12, 8))
#     sns.boxplot(x='StreetLight', y=approach, data=df)
#     plt.title(f'Comparison of {approach} by Street Light')
#     plt.show()

# Scatter plot para ver cómo afecta la posición de la raíz
# for approach in approaches:
#     plt.figure(figsize=(12, 8))
#     sns.scatterplot(x='RootX', y='RootY', hue='StreetLight', style='StreetLight', size=approach, sizes=(20, 200), data=df, legend='full')
#     plt.title(f'Root Position vs Street Light for {approach}')
#     plt.xlabel('RootX')
#     plt.ylabel('RootY')
#     plt.legend(title='StreetLight')
#     plt.show()

# CDF plot for each street light, showing all approaches
# approaches = ['RPL', 'Optimized RPL', 'Projected Routes', 'Proposed Solution']
approaches = ['Projected Routes - Edges removed', 'Projected Routes - Disjoint Paths', 'Proposed Solution - Edges removed', 'Proposed Solution - Disjoint paths', 'Proposed Solution - Common Neighbor Domain']

for sl_id in df['StreetLight'].unique():
    plt.figure(figsize=(12, 8))
    subset = df[df['StreetLight'] == sl_id]

    for approach in approaches:
        sns.ecdfplot(data=subset, x=approach, label=approach)

    # Annotate Projected Routes and Domain 1 with exact values
    # projected_routes_value = subset['Projected Routes'].unique()[0]
    # # proposed_solution_value = subset['Proposed Solution'].unique()[0]
    # proposed_solution_value_1 = subset['Proposed Solution - Track Domain'].unique()[0]
    # proposed_solution_value_2 = subset['Proposed Solution - Common Neighbor Domain'].unique()[0]
    # 
    # plt.axvline(x=projected_routes_value, color='blue', linestyle='--')
    # plt.text(projected_routes_value, 0.5, f'{projected_routes_value}', color='blue', va='center')
    # 
    # plt.axvline(x=proposed_solution_value, color='green', linestyle='--')
    # plt.text(proposed_solution_value, 0.5, f'{proposed_solution_value}', color='green', va='center')
# 
    # plt.axvline(x=proposed_solution_value, color='green', linestyle='--')
    # plt.text(proposed_solution_value, 0.5, f'{proposed_solution_value}', color='green', va='center')
    
    plt.title(f'Cumulative Distribution Function of Approaches for Street Light {sl_id}')
    plt.xlabel('Number of Transmissions')
    plt.ylabel('Cumulative Probability')
    plt.legend(title='Approach')
    plt.show()

approaches2 = ['RPL', 'Optimized RPL']

# Scatter plot separado por street light y approach
import matplotlib.colors as mcolors


def show_scatter_plot(df):
    # Scatter plot separado por street light y approach
    for sl_id in df['StreetLight'].unique():
        for approach in approaches2:
            plt.figure(figsize=(12, 8))
            subset = df[df['StreetLight'] == sl_id]

            # Get the min and max values for the approach to set the color scale
            vmin = subset[approach].min()
            vmax = subset[approach].max()

            # Handle edge cases where vmin == vmax
            if vmin == vmax:
                vmax += 1

            # Create the scatter plot with color bar
            norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
            cmap = plt.get_cmap('viridis')

            scatter = plt.scatter(subset['RootX'], subset['RootY'], c=subset[approach], cmap=cmap, norm=norm)

            # Add a color bar with the correct range
            cbar = plt.colorbar(scatter, label=f'{approach} Value')
            cbar.set_ticks(np.linspace(vmin, vmax, num=6))
            cbar.set_ticklabels([f"{tick:.2f}" for tick in np.linspace(vmin, vmax, num=6)])

            plt.title(f'Root Position vs {approach} for Street Light {sl_id}')
            plt.xlabel('RootX')
            plt.ylabel('RootY')
            plt.show()

#show_scatter_plot(df)