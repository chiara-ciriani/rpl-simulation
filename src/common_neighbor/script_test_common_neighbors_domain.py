import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from .test_common_neighbors_domain import calculate_metrics_common_neighbors_domain

NUM_STREET_LIGHTS = 11

width = 65
height = 30
num_nodes = 200
tx_range = 10
max_distance = 5

# Number of transmissions
all_results = []

# Min cut
data_vertex_cut = []
data_edge_cut = []

# Probabilities
data_source_0 = []
data_source_5 = []
data_source_10 = []

# Length of domains
domain_lengths_data = []

# Recolectar datos para estadísticas
for _ in range(200):
    results = calculate_metrics_common_neighbors_domain(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, False)
    
    # Número de transmisiones
    all_results.append(results['transmissions'])

    # Min cut
    data_vertex_cut.append({
        'Common Neighbor Domain': results['min_cuts']['domain1']['vertex_cut'],
        'Common Neighbor Range Extended Domain': results['min_cuts']['domain2']['vertex_cut'],
        'Common Neighbor Optimized with MST Domain': results['min_cuts']['domain3']['vertex_cut'],
        'Cluster Based Domain': results['min_cuts']['domain4']['vertex_cut']
    })
    
    data_edge_cut.append({
        'Common Neighbor Domain': results['min_cuts']['domain1']['edge_cut'],
        'Common Neighbor Range Extended Domain': results['min_cuts']['domain2']['edge_cut'],
        'Common Neighbor Optimized with MST Domain': results['min_cuts']['domain3']['edge_cut'],
        'Cluster Based Domain': results['min_cuts']['domain4']['edge_cut']
    })

    # Probabilidades
    data_source_0.append({
        'Common Neighbor Domain': results['probabilities']['source_0']['domain1'],
        'Common Neighbor Range Extended Domain': results['probabilities']['source_0']['domain2'],
        'Common Neighbor Optimized with MST Domain': results['probabilities']['source_0']['domain3'],
        'Cluster Based Domain': results['probabilities']['source_0']['domain4']
    })
    
    data_source_5.append({
        'Common Neighbor Domain': results['probabilities']['source_5']['domain1'],
        'Common Neighbor Range Extended Domain': results['probabilities']['source_5']['domain2'],
        'Common Neighbor Optimized with MST Domain': results['probabilities']['source_5']['domain3'],
        'Cluster Based Domain': results['probabilities']['source_5']['domain4']
    })
    
    data_source_10.append({
        'Common Neighbor Domain': results['probabilities']['source_10']['domain1'],
        'Common Neighbor Range Extended Domain': results['probabilities']['source_10']['domain2'],
        'Common Neighbor Optimized with MST Domain': results['probabilities']['source_10']['domain3'],
        'Cluster Based Domain': results['probabilities']['source_10']['domain4']
    })

    # Longitudes de los dominios
    domain_lengths_data.append({
        'Common Neighbor Domain': results['domain_lengths']['domain1'],
        'Common Neighbor Range Extended Domain': results['domain_lengths']['domain2'],
        'Common Neighbor Optimized with MST Domain': results['domain_lengths']['domain3'],
        'Cluster Based Domain': results['domain_lengths']['domain4']
    })



# NUMBER OF TRANSMISSIONS
data = []
for results in all_results:
    for sl_id, values in results.items():
        data.append({
            'StreetLight': sl_id,
            'Common Neighbor Domain': values['domain1'],
            'Common Neighbor Range Extended Domain': values['domain2'],
            'Common Neighbor Optimized with MST Domain': values['domain3'],
            'Cluster Based Domain': values['domain4'],
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

# CDF plot for each street light, showing all approaches
# approaches = ['RPL', 'Optimized RPL', 'Projected Routes', 'Proposed Solution']
approaches = ['Common Neighbor Domain', 'Common Neighbor Range Extended Domain', 'Common Neighbor Optimized with MST Domain', 'Cluster Based Domain']

for sl_id in df['StreetLight'].unique():
    plt.figure(figsize=(12, 8))
    subset = df[df['StreetLight'] == sl_id]

    for approach in approaches:
        sns.ecdfplot(data=subset, x=approach, label=approach)
    
    plt.title(f'Cumulative Distribution Function of Approaches for Street Light {sl_id}')
    plt.xlabel('Number of Transmissions')
    plt.ylabel('Cumulative Probability')
    plt.legend(title='Approach')
    plt.show()


# PROBABILITIES

df_source_0 = pd.DataFrame(data_source_0)
df_source_5 = pd.DataFrame(data_source_5)
df_source_10 = pd.DataFrame(data_source_10)

# Calculate mean and variance for each source
mean_variance_stats = []
approaches = ['Common Neighbor Domain', 'Common Neighbor Range Extended Domain', 'Common Neighbor Optimized with MST Domain', 'Cluster Based Domain']

for df, source in zip([df_source_0, df_source_5, df_source_10], ['SL 0', 'SL 5', 'SL 10']):
    for approach in approaches:
        mean_value = df[approach].mean()
        variance_value = df[approach].var()
        mean_variance_stats.append({
            'Source': source,
            'Approach': approach,
            'Mean': mean_value,
            'Variance': variance_value
        })

df_stats = pd.DataFrame(mean_variance_stats)

print("Mean and Variance Statistics:")
print(df_stats)

# Graficar el CDF para cada origen (SL 0, SL 5, SL 10)

plt.figure(figsize=(12, 8))
for approach in approaches:
    sns.ecdfplot(data=df_source_0, x=approach, label=approach)
plt.title('CDF in a network of 200 nodes and 11 street lights')
plt.xlabel('Probability that all street lights receive message from SL 0')
plt.ylabel('Cumulative Probability')
plt.legend(title='Domain')
plt.show()

plt.figure(figsize=(12, 8))
for approach in approaches:
    sns.ecdfplot(data=df_source_5, x=approach, label=approach)
plt.title('CDF in a network of 200 nodes and 11 street lights')
plt.xlabel('Probability that all street lights receive message from SL 5')
plt.ylabel('Cumulative Probability')
plt.legend(title='Domain')
plt.show()

plt.figure(figsize=(12, 8))
for approach in approaches:
    sns.ecdfplot(data=df_source_10, x=approach, label=approach)
plt.title('CDF in a network of 200 nodes and 11 street lights')
plt.xlabel('Probability that all street lights receive message from SL 10')
plt.ylabel('Cumulative Probability')
plt.legend(title='Domain')
plt.show()

# MIN CUT

# Convertir los datos a DataFrames para cortes de vértices y aristas
df_vertex_cut = pd.DataFrame(data_vertex_cut)
df_edge_cut = pd.DataFrame(data_edge_cut)

print(df_vertex_cut)
print("")
print("----")
print("")
print(df_edge_cut)

# Lista de enfoques a comparar
approaches = ['Common Neighbor Domain', 'Common Neighbor Range Extended Domain', 'Common Neighbor Optimized with MST Domain', 'Cluster Based Domain']

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

# GRAFICAR LONGITUDES DE DOMINIOS

df_domain_lengths = pd.DataFrame(domain_lengths_data)
df_domain_lengths = df_domain_lengths.melt(var_name='Domain', value_name='Length')

plt.figure(figsize=(10, 6))
sns.boxplot(x='Domain', y='Length', data=df_domain_lengths)
plt.title('Comparison of Domain Lengths')
plt.xlabel('Domain Type')
plt.ylabel('Length (Number of Nodes)')
plt.show()