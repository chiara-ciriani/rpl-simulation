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
        'Disjoint paths domain': results['min_vertex_cut_domain2'],
        'Common Neighbor domain': results['min_vertex_cut_domain3']
    })
    
    data_edge_cut.append({
        'Edges removed domain': results['min_edge_cut_domain1'],
        'Disjoint paths domain': results['min_edge_cut_domain2'],
        'Common Neighbor domain': results['min_edge_cut_domain3']
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

# Graficar el CDF para Min Vertex Cut

plt.figure(figsize=(12, 8))
for approach in approaches:
    sns.ecdfplot(data=df_vertex_cut, x=approach, label=approach)
plt.title('CDF in a network of 200 nodes and 11 street lights')
plt.xlabel('Min Vertex Cut')
plt.ylabel('Cumulative Probability')
plt.legend(title='Domain')
plt.show()

# Graficar el CDF para Min Edge Cut

plt.figure(figsize=(12, 8))
for approach in approaches:
    sns.ecdfplot(data=df_edge_cut, x=approach, label=approach)
plt.title('CDF in a network of 200 nodes and 11 street lights')
plt.xlabel('Min Edge Cut')
plt.ylabel('Cumulative Probability')
plt.legend(title='Domain')
plt.show()
