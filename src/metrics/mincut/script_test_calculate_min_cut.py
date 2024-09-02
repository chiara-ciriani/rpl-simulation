import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from .test_calculate_min_cut import test_calculate_min_cut

NUM_STREET_LIGHTS = 11

width = 65
height = 50
num_nodes = 200
tx_range = 10
max_distance = 5 

# Inicializar listas para almacenar los resultados de min cut
data_vertex_cut = []
data_edge_cut = []

# Realiza múltiples simulaciones para recopilar datos
for _ in range(200):
    results = test_calculate_min_cut(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, False)
    
    data_vertex_cut.append({
        'Edges removed domain': results['min_vertex_cut_domain1'],
        'Common Neighbor domain': results['min_vertex_cut_domain2'],
        'Disjoint paths domain': results['min_vertex_cut_domain3']
    })
    
    data_edge_cut.append({
        'Edges removed domain': results['min_edge_cut_domain1'],
        'Common Neighbor domain': results['min_edge_cut_domain2'],
        'Disjoint paths domain': results['min_edge_cut_domain3']
    })

# Convertir los datos a DataFrames para cortes de vértices y aristas
df_vertex_cut = pd.DataFrame(data_vertex_cut)
df_edge_cut = pd.DataFrame(data_edge_cut)

print(df_vertex_cut)
print("")
print("----")
print("")
print(df_edge_cut)

# Lista de enfoques a comparar
approaches = ['Edges removed domain', 'Disjoint paths domain', 'Common Neighbor domain']

# Calculate percentages for each approach for Min Vertex Cut
vertex_cut_percentages = {
    'Approach': [],
}

# Calculate unique values dynamically for Vertex Cut
unique_vertex_values = pd.concat([df_vertex_cut[approach] for approach in approaches]).unique()
unique_vertex_values.sort()

# Initialize the dictionary with unique values
for val in unique_vertex_values:
    vertex_cut_percentages[f'Percentage of {val}'] = []

for approach in approaches:
    counts = df_vertex_cut[approach].value_counts(normalize=True) * 100  # Calculate percentage
    vertex_cut_percentages['Approach'].append(approach)
    for val in unique_vertex_values:
        vertex_cut_percentages[f'Percentage of {val}'].append(counts.get(val, 0))

df_vertex_percentages = pd.DataFrame(vertex_cut_percentages)
print(df_vertex_percentages)

# Calculate percentages for each approach for Min Edge Cut
edge_cut_percentages = {
    'Approach': [],
}

# Calculate unique values dynamically for Edge Cut
unique_edge_values = pd.concat([df_edge_cut[approach] for approach in approaches]).unique()
unique_edge_values.sort()

# Initialize the dictionary with unique values
for val in unique_edge_values:
    edge_cut_percentages[f'Percentage of {val}'] = []

for approach in approaches:
    counts = df_edge_cut[approach].value_counts(normalize=True) * 100  # Calculate percentage
    edge_cut_percentages['Approach'].append(approach)
    for val in unique_edge_values:
        edge_cut_percentages[f'Percentage of {val}'].append(counts.get(val, 0))

df_edge_percentages = pd.DataFrame(edge_cut_percentages)
print(df_edge_percentages)

# Plot the results for Min Vertex Cut
# plt.figure(figsize=(12, 8))
# bottom_vals = [0] * len(df_vertex_percentages)  # Initialize bottom values for stacking
# for val in unique_vertex_values:
#     sns.barplot(x='Approach', y=f'Percentage of {val}', data=df_vertex_percentages, label=f'Percentage of {val}', bottom=bottom_vals)
#     bottom_vals += df_vertex_percentages[f'Percentage of {val}'].values  # Update bottom for next stack
# 
# plt.title('Min Vertex Cut Percentages in a network of 200 nodes and 11 street lights')
# plt.ylabel('Percentage')
# plt.legend(title='Min Vertex Cut Value')
# plt.show()
# 
# # Plot the results for Min Edge Cut
# plt.figure(figsize=(12, 8))
# bottom_vals = [0] * len(df_edge_percentages)  # Initialize bottom values for stacking
# for val in unique_edge_values:
#     sns.barplot(x='Approach', y=f'Percentage of {val}', data=df_edge_percentages, label=f'Percentage of {val}', bottom=bottom_vals)
#     bottom_vals += df_edge_percentages[f'Percentage of {val}'].values  # Update bottom for next stack
# 
# plt.title('Min Edge Cut Percentages in a network of 200 nodes and 11 street lights')
# plt.ylabel('Percentage')
# plt.legend(title='Min Edge Cut Value')
# plt.show()
# 