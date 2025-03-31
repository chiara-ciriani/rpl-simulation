from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from test_domains_metrics import calculate_metrics

NUM_STREET_LIGHTS = 11

DIRECT_COMUNICATION=False

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
for _ in range(100):
    results = calculate_metrics(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, DIRECT_COMUNICATION, False)
    
    # Número de transmisiones
    all_results.append(results['transmissions'])

    # Min cut
    data_vertex_cut.append({
        'Eliminación de aristas': results['min_cuts']['domain1']['vertex_cut'],
        'Vecino común': results['min_cuts']['domain2']['vertex_cut'],
        'Eliminación de nodos': results['min_cuts']['domain3']['vertex_cut']
    })
    
    data_edge_cut.append({
        'Eliminación de aristas': results['min_cuts']['domain1']['edge_cut'],
        'Vecino común': results['min_cuts']['domain2']['edge_cut'],
        'Eliminación de nodos': results['min_cuts']['domain3']['edge_cut']
    })

    # # Probabilidades
    # data_source_0.append({
    #     'Eliminación de aristas': results['probabilities']['source_0']['domain1'],
    #     'Eliminación de nodos': results['probabilities']['source_0']['domain3'],
    #     'Vecino común': results['probabilities']['source_0']['domain2']
    # })
    
    # data_source_5.append({
    #     'Eliminación de aristas': results['probabilities']['source_5']['domain1'],
    #     'Eliminación de nodos': results['probabilities']['source_5']['domain3'],
    #     'Vecino común': results['probabilities']['source_5']['domain2']
    # })
    # 
    # data_source_10.append({
    #     'Eliminación de aristas': results['probabilities']['source_10']['domain1'],
    #     'Eliminación de nodos': results['probabilities']['source_10']['domain3'],
    #     'Vecino común': results['probabilities']['source_10']['domain2']
    # })

    # Longitudes de los dominios
    domain_lengths_data.append({
        'Eliminación de aristas': results['domain_lengths']['domain1'],
        'Vecino común': results['domain_lengths']['domain2'],
        'Eliminación de nodos': results['domain_lengths']['domain3']
    })



# NUMBER OF TRANSMISSIONS
data = []
for results in all_results:
    for sl_id, values in results.items():
        data.append({
            'StreetLight': sl_id,
            'Projected Routes: Edges Removed': values['projected_routes1'],
            'Projected Routes: Nodes Removed': values['projected_routes2'],
            'Proposed Solution: Edges Removed': values['domain1'],
            'Proposed Solution: Nodes Removed': values['domain3'],
            'Proposed Solution: Common Neighbor': values['domain2'],
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
# approaches = ['Projected Routes: Edges Removed', 'Projected Routes: Nodes Removed', 'Proposed Solution: Edges Removed', 'Proposed Solution: Nodes Removed', 'Proposed Solution: Common Neighbor']
# 
# for sl_id in df['StreetLight'].unique():
#     subset = df[df['StreetLight'] == sl_id]
# 
#     for approach in approaches:
#         sns.ecdfplot(data=subset, x=approach, label=approach)
#     
#     # Update title and labels with a larger font size
#     plt.title(f'Cumulative Distribution Function of Approaches for Street Light {sl_id}', fontsize=14)
#     plt.xlabel('Number of Transmissions', fontsize=14)
#     plt.ylabel('Cumulative Probability', fontsize=12)
# 
#     # Increase the font size for tick labels
#     plt.tick_params(axis='both', which='major', labelsize=14)
# 
#     # Add grid lines only for the horizontal direction
#     plt.grid(axis='y', linestyle='--', linewidth=0.7)
# 
#     plt.legend(title='Approach', fontsize=12, title_fontsize=14)
#     plt.show()


# PROBABILITIES

df_source_0 = pd.DataFrame(data_source_0)
df_source_5 = pd.DataFrame(data_source_5)
df_source_10 = pd.DataFrame(data_source_10)

# Calculate mean and variance for each source
mean_variance_stats = []
approaches = ['Eliminación de aristas', 'Eliminación de nodos', 'Vecino común']
colors = {
    'Eliminación de aristas': 'blue',
    'Eliminación de nodos': 'violet',
    'Vecino común': 'orange'
}
markers = {
'Eliminación de aristas': 'o',  # Circulo
'Eliminación de nodos': "X",  # X
'Vecino común': '^'  # Triángulo
}
marker_size = 50

# for df, source in zip([df_source_0, df_source_5, df_source_10], ['SL 0', 'SL 5', 'SL 10']):
#     for approach in approaches:
#         mean_value = df[approach].mean()
#         variance_value = df[approach].var()
#         mean_variance_stats.append({
#             'Source': source,
#             'Approach': approach,
#             'Mean': mean_value,
#             'Variance': variance_value
#         })
# 
# df_stats = pd.DataFrame(mean_variance_stats)
# 
# print("Mean and Variance Statistics:")
# print(df_stats)
# 
# # Graficar el CDF para cada origen (SL 0, SL 5, SL 10)
# 
# plt.figure(figsize=(10, 6))
# 
# # Tamaño fijo de la figura en pulgadas
# FIGURE_SIZE = (8, 5)  # Ancho x Alto en pulgadas
# DPI = 300  # Resolución en puntos por pulgada
# X_LIMITS = (0, 1)  # Límite fijo para el eje X
# Y_LIMITS = (0, 1)  # Límite fijo para el eje Y
# X_TICKS = np.linspace(0, 1, 6)  # Divisiones uniformes en X
# Y_TICKS = np.linspace(0, 1, 6)  # Divisiones uniformes en Y
# 
# # Almacenar elementos de leyenda
# legend_elements = []
# 
# plt.figure(figsize=FIGURE_SIZE)
# 
# for approach in approaches:
#     sns.ecdfplot(
#         data=df_source_0,
#         x=approach, 
#         label=approach, 
#         color=colors[approach],    # Asignar color
#     )
# 
#     # Calcular manualmente el ECDF
#     x_values = np.sort(df_source_0[approach].values)
#     y_values = np.arange(1, len(x_values)+1) / len(x_values)
#     # Dibujar los marcadores solo en puntos espaciados (por ejemplo, cada 10 puntos)
#     marker_indices = np.arange(0, len(x_values), 5)  # Cambia el 10 para ajustar la separación
#     
#     plt.scatter(
#         x_values[marker_indices], 
#         y_values[marker_indices], 
#         color=colors[approach], 
#         marker=markers[approach], 
#         s=marker_size
#     )
#     
#     # Agregar tanto la línea como el marcador a la leyenda
#     legend_elements.append(Line2D([0], [0], color=colors[approach], lw=2, 
#                               label=approach, marker=markers[approach], 
#                               markersize=10, markerfacecolor=colors[approach], 
#                               markeredgewidth=0))  # Esto agrega tanto la línea como el marcador
#     
# plt.xlim(X_LIMITS)
# plt.ylim(Y_LIMITS)
# plt.xticks(X_TICKS)
# plt.yticks(Y_TICKS)
# 
# plt.xlabel('Probabilidad que todos los faroles se enciendan desde el farol 0', fontsize=14)
# plt.ylabel('Probabilidad acumuluada', fontsize=12)
# # Increase the font size for tick labels
# plt.tick_params(axis='both', which='major', labelsize=14)
# # Add grid lines only for the horizontal direction
# plt.grid(axis='y', linestyle='--', linewidth=0.7)
# # Crear una lista de elementos de la leyenda
# legend_elements = [Line2D([0], [0], marker=markers[approach], color='w',
#                            label=approach, markerfacecolor=colors[approach], markersize=10)
#                    for approach in approaches]
# 
# # Mostrar la leyenda
# plt.legend(handles=legend_elements, fontsize=12)
# plt.show()
# 
# plt.figure(figsize=FIGURE_SIZE)
# 
# # Almacenar elementos de leyenda
# legend_elements = []
# 
# for approach in approaches:
#     sns.ecdfplot(
#         data=df_source_5,
#         x=approach, 
#         label=approach, 
#         color=colors[approach],    # Asignar color
#     )
# 
#     # Calcular manualmente el ECDF
#     x_values = np.sort(df_source_5[approach].values)
#     y_values = np.arange(1, len(x_values)+1) / len(x_values)
#     # Dibujar los marcadores solo en puntos espaciados (por ejemplo, cada 10 puntos)
#     marker_indices = np.arange(0, len(x_values), 5)  # Cambia el 10 para ajustar la separación
#     
#     plt.scatter(
#         x_values[marker_indices], 
#         y_values[marker_indices], 
#         color=colors[approach], 
#         marker=markers[approach], 
#         s=marker_size
#     )
#     
#     # Agregar tanto la línea como el marcador a la leyenda
#     legend_elements.append(Line2D([0], [0], color=colors[approach], lw=2, 
#                               label=approach, marker=markers[approach], 
#                               markersize=10, markerfacecolor=colors[approach], 
#                               markeredgewidth=0))  # Esto agrega tanto la línea como el marcador
#     
# plt.xlim(X_LIMITS)
# plt.ylim(Y_LIMITS)
# plt.xticks(X_TICKS)
# plt.yticks(Y_TICKS)
# 
# plt.xlabel('Probabilidad que todos los faroles se enciendan desde el farol 5', fontsize=14)
# plt.ylabel('Probabilidad acumuluada', fontsize=12)
# # Increase the font size for tick labels
# plt.tick_params(axis='both', which='major', labelsize=14)
# # Add grid lines only for the horizontal direction
# plt.grid(axis='y', linestyle='--', linewidth=0.7)
# # Crear una lista de elementos de la leyenda
# legend_elements = [Line2D([0], [0], marker=markers[approach], color='w',
#                            label=approach, markerfacecolor=colors[approach], markersize=10)
#                    for approach in approaches]
# 
# # Mostrar la leyenda
# plt.legend(handles=legend_elements, fontsize=12)
# plt.show()
# 
# plt.figure(figsize=FIGURE_SIZE)
# 
# # Almacenar elementos de leyenda
# legend_elements = []
# 
# for approach in approaches:
#     sns.ecdfplot(
#         data=df_source_10,
#         x=approach, 
#         label=approach, 
#         color=colors[approach],    # Asignar color
#     )
# 
#     # Calcular manualmente el ECDF
#     x_values = np.sort(df_source_10[approach].values)
#     y_values = np.arange(1, len(x_values)+1) / len(x_values)
#     # Dibujar los marcadores solo en puntos espaciados (por ejemplo, cada 10 puntos)
#     marker_indices = np.arange(0, len(x_values), 5)  # Cambia el 10 para ajustar la separación
#     
#     plt.scatter(
#         x_values[marker_indices], 
#         y_values[marker_indices], 
#         color=colors[approach], 
#         marker=markers[approach], 
#         s=marker_size
#     )
#     
#     # Agregar tanto la línea como el marcador a la leyenda
#     legend_elements.append(Line2D([0], [0], color=colors[approach], lw=2, 
#                               label=approach, marker=markers[approach], 
#                               markersize=10, markerfacecolor=colors[approach], 
#                               markeredgewidth=0))  # Esto agrega tanto la línea como el marcador
#     
# plt.xlim(X_LIMITS)
# plt.ylim(Y_LIMITS)
# plt.xticks(X_TICKS)
# plt.yticks(Y_TICKS)
# 
# plt.xlabel('Probabilidad que todos los faroles se enciendan desde el farol 10', fontsize=14)
# plt.ylabel('Probabilidad acumuluada', fontsize=12)
# # Increase the font size for tick labels
# plt.tick_params(axis='both', which='major', labelsize=14)
# # Add grid lines only for the horizontal direction
# plt.grid(axis='y', linestyle='--', linewidth=0.7)
# # Crear una lista de elementos de la leyenda
# legend_elements = [Line2D([0], [0], marker=markers[approach], color='w',
#                            label=approach, markerfacecolor=colors[approach], markersize=10)
#                    for approach in approaches]
# 
# # Mostrar la leyenda
# plt.legend(handles=legend_elements, fontsize=12)
# plt.show()

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
approaches = ['Eliminación de aristas', 'Eliminación de nodos', 'Vecino común']

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