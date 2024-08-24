import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from test_calculate_min_cut import test_calculate_min_cut

NUM_STREET_LIGHTS = 11

width = 65
height = 50
num_nodes = 200
tx_range = 5 
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
    'Percentage of 1': [],
    'Percentage of 2': [],
    'Percentage of 3': []
}

for approach in approaches:
    counts = df_vertex_cut[approach].value_counts(normalize=True) * 100  # Calculate percentage
    vertex_cut_percentages['Approach'].append(approach)
    vertex_cut_percentages['Percentage of 1'].append(counts.get(1, 0))
    vertex_cut_percentages['Percentage of 2'].append(counts.get(2, 0))
    vertex_cut_percentages['Percentage of 3'].append(counts.get(3, 0))

df_vertex_percentages = pd.DataFrame(vertex_cut_percentages)
print(df_vertex_percentages)

# Calculate percentages for each approach for Min Edge Cut
edge_cut_percentages = {
    'Approach': [],
    'Percentage of 1': [],
    'Percentage of 2': [],
    'Percentage of 3': []
}

for approach in approaches:
    counts = df_edge_cut[approach].value_counts(normalize=True) * 100  # Calculate percentage
    edge_cut_percentages['Approach'].append(approach)
    edge_cut_percentages['Percentage of 1'].append(counts.get(1, 0))
    edge_cut_percentages['Percentage of 2'].append(counts.get(2, 0))
    edge_cut_percentages['Percentage of 3'].append(counts.get(3, 0))

df_edge_percentages = pd.DataFrame(edge_cut_percentages)
print(df_edge_percentages)

# Plot the results for Min Vertex Cut
plt.figure(figsize=(12, 8))
sns.barplot(x='Approach', y='Percentage of 1', data=df_vertex_percentages, color='blue', label='Percentage of 1')
sns.barplot(x='Approach', y='Percentage of 2', data=df_vertex_percentages, color='orange', label='Percentage of 2', bottom=df_vertex_percentages['Percentage of 1'])
sns.barplot(x='Approach', y='Percentage of 3', data=df_vertex_percentages, color='green', label='Percentage of 3', bottom=df_vertex_percentages['Percentage of 1'] + df_vertex_percentages['Percentage of 2'])
plt.title('Min Vertex Cut Percentages in a network of 200 nodes and 11 street lights')
plt.ylabel('Percentage')
plt.legend(title='Min Vertex Cut Value')
plt.show()

# Plot the results for Min Edge Cut
plt.figure(figsize=(12, 8))
sns.barplot(x='Approach', y='Percentage of 1', data=df_edge_percentages, color='blue', label='Percentage of 1')
sns.barplot(x='Approach', y='Percentage of 2', data=df_edge_percentages, color='orange', label='Percentage of 2', bottom=df_edge_percentages['Percentage of 1'])
sns.barplot(x='Approach', y='Percentage of 3', data=df_edge_percentages, color='green', label='Percentage of 3', bottom=df_edge_percentages['Percentage of 1'] + df_edge_percentages['Percentage of 2'])
plt.title('Min Edge Cut Percentages in a network of 200 nodes and 11 street lights')
plt.ylabel('Percentage')
plt.legend(title='Min Edge Cut Value')
plt.show()
