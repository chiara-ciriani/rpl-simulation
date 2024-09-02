import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from test_domains_metrics import calculate_metrics

NUM_STREET_LIGHTS = 11

DIRECT_COMUNICATION=True

if DIRECT_COMUNICATION:
    width = 2500
    height = 1800
    num_nodes = 200
    tx_range = 200
    max_distance = 200
else:
    width = 2500
    height = 2000
    num_nodes = 200
    tx_range = 400
    max_distance = 200

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
    results = calculate_metrics(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, DIRECT_COMUNICATION, False)
    
    # Número de transmisiones
    all_results.append(results['transmissions'])

    # Min cut
    data_vertex_cut.append({
        'Edges removed domain': results['min_cuts']['domain1']['vertex_cut'],
        'Common Neighbor domain': results['min_cuts']['domain2']['vertex_cut'],
        'Disjoint paths domain': results['min_cuts']['domain3']['vertex_cut']
    })
    
    data_edge_cut.append({
        'Edges removed domain': results['min_cuts']['domain1']['edge_cut'],
        'Common Neighbor domain': results['min_cuts']['domain2']['edge_cut'],
        'Disjoint paths domain': results['min_cuts']['domain3']['edge_cut']
    })

    # Probabilidades
    data_source_0.append({
        'Edges removed domain': results['probabilities']['source_0']['domain1'],
        'Disjoint paths domain': results['probabilities']['source_0']['domain3'],
        'Common Neighbor domain': results['probabilities']['source_0']['domain2']
    })
    
    data_source_5.append({
        'Edges removed domain': results['probabilities']['source_5']['domain1'],
        'Disjoint paths domain': results['probabilities']['source_5']['domain3'],
        'Common Neighbor domain': results['probabilities']['source_5']['domain2']
    })
    
    data_source_10.append({
        'Edges removed domain': results['probabilities']['source_10']['domain1'],
        'Disjoint paths domain': results['probabilities']['source_10']['domain3'],
        'Common Neighbor domain': results['probabilities']['source_10']['domain2']
    })

    # Longitudes de los dominios
    domain_lengths_data.append({
        'Edges removed domain': results['domain_lengths']['domain1'],
        'Common Neighbor domain': results['domain_lengths']['domain2'],
        'Disjoint paths domain': results['domain_lengths']['domain3']
    })



# NUMBER OF TRANSMISSIONS
data = []
for results in all_results:
    for sl_id, values in results.items():
        data.append({
            'StreetLight': sl_id,
            'Projected Routes - Edges removed': values['projected_routes1'],
            'Projected Routes - Disjoint Paths': values['projected_routes2'],
            'Proposed Solution - Edges removed': values['domain1'],
            'Proposed Solution - Disjoint paths': values['domain3'],
            'Proposed Solution - Common Neighbor Domain': values['domain2'],
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
approaches = ['Projected Routes - Edges removed', 'Projected Routes - Disjoint Paths', 'Proposed Solution - Edges removed', 'Proposed Solution - Disjoint paths', 'Proposed Solution - Common Neighbor Domain']

for sl_id in df['StreetLight'].unique():
    subset = df[df['StreetLight'] == sl_id]

    for approach in approaches:
        sns.ecdfplot(data=subset, x=approach, label=approach)
    
    # Update title and labels with a larger font size
    plt.title(f'Cumulative Distribution Function of Approaches for Street Light {sl_id}', fontsize=14)
    plt.xlabel('Number of Transmissions', fontsize=14)
    plt.ylabel('Cumulative Probability', fontsize=12)

    # Increase the font size for tick labels
    plt.tick_params(axis='both', which='major', labelsize=14)

    # Add grid lines only for the horizontal direction
    plt.grid(axis='y', linestyle='--', linewidth=0.7)

    plt.legend(title='Approach', fontsize=12, title_fontsize=14)
    plt.show()


# PROBABILITIES

df_source_0 = pd.DataFrame(data_source_0)
df_source_5 = pd.DataFrame(data_source_5)
df_source_10 = pd.DataFrame(data_source_10)

# Calculate mean and variance for each source
mean_variance_stats = []
approaches = ['Edges removed domain', 'Disjoint paths domain', 'Common Neighbor domain']

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

for approach in approaches:
    sns.ecdfplot(data=df_source_0, x=approach, label=approach)
plt.title('CDF in a network of 200 nodes and 11 street lights', fontsize=14)
plt.xlabel('Probability that all street lights receive message from SL 0', fontsize=14)
plt.ylabel('Cumulative Probability', fontsize=12)
# Increase the font size for tick labels
plt.tick_params(axis='both', which='major', labelsize=14)
# Add grid lines only for the horizontal direction
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.legend(title='Domain', fontsize=12, title_fontsize=14)
plt.show()

for approach in approaches:
    sns.ecdfplot(data=df_source_5, x=approach, label=approach)
plt.title('CDF in a network of 200 nodes and 11 street lights', fontsize=14)
plt.xlabel('Probability that all street lights receive message from SL 5', fontsize=14)
plt.ylabel('Cumulative Probability', fontsize=12)
# Increase the font size for tick labels
plt.tick_params(axis='both', which='major', labelsize=14)
# Add grid lines only for the horizontal direction
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.legend(title='Domain', fontsize=12, title_fontsize=14)
plt.show()

for approach in approaches:
    sns.ecdfplot(data=df_source_10, x=approach, label=approach)
plt.title('CDF in a network of 200 nodes and 11 street lights', fontsize=14)
plt.xlabel('Probability that all street lights receive message from SL 10', fontsize=14)
plt.ylabel('Cumulative Probability', fontsize=12)
# Increase the font size for tick labels
plt.tick_params(axis='both', which='major', labelsize=14)
# Add grid lines only for the horizontal direction
plt.grid(axis='y', linestyle='--', linewidth=0.7)
plt.legend(title='Domain', fontsize=12, title_fontsize=14)
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

# GRAFICAR LONGITUDES DE DOMINIOS

df_domain_lengths = pd.DataFrame(domain_lengths_data)
df_domain_lengths = df_domain_lengths.melt(var_name='Domain', value_name='Length')

plt.figure(figsize=(10, 6))
sns.boxplot(x='Domain', y='Length', data=df_domain_lengths)
plt.title('Comparison of Domain Lengths')
plt.xlabel('Domain Type')
plt.ylabel('Length (Number of Nodes)')
plt.show()