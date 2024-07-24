from test_domains_dio import send_to_all_street_lights
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

NUM_STREET_LIGHTS=11

width = 30
height = 30
num_nodes = 20 
tx_range = 10 
max_distance = 10 

all_results = []

for _ in range(500):
    results, root_position = send_to_all_street_lights(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, False)
    all_results.append((results, root_position))

# AGREGAR TAMBIEN MISMO GRAFICO QUE ANTESSS

data = []
for results, root_position in all_results:
    for sl_id, values in results.items():
        data.append({
            'StreetLight': sl_id,
            'RPL': values[0],
            'Optimized RPL': values[1],
            'Projected Routes': values[2],
            'Domain 1': values[3],
            'Domain 2': values[4],
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
approaches = ['RPL', 'Optimized RPL', 'Projected Routes', 'Domain 1', 'Domain 2']
for approach in approaches:
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='StreetLight', y=approach, data=df)
    plt.title(f'Comparison of {approach} by Street Light')
    plt.show()

# Scatter plot para ver cómo afecta la posición de la raíz
# for approach in approaches:
#     plt.figure(figsize=(12, 8))
#     sns.scatterplot(x='RootX', y='RootY', hue='StreetLight', style='StreetLight', size=approach, sizes=(20, 200), data=df, legend='full')
#     plt.title(f'Root Position vs Street Light for {approach}')
#     plt.xlabel('RootX')
#     plt.ylabel('RootY')
#     plt.legend(title='StreetLight')
#     plt.show()

# Scatter plot separado por street light y approach
for sl_id in df['StreetLight'].unique():
    for approach in approaches:
        plt.figure(figsize=(12, 8))
        subset = df[df['StreetLight'] == sl_id]

        # Crear el scatter plot
        sns.scatterplot(x='RootX', y='RootY', hue=approach, palette='viridis', data=subset, legend='full')

        plt.title(f'Root Position vs {approach} for Street Light {sl_id}')
        plt.xlabel('RootX')
        plt.ylabel('RootY')
        plt.legend(title=approach)
        plt.show()
