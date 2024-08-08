import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from test_domains_probabilities import calculate_probabilities

NUM_STREET_LIGHTS = 11

width = 65
height = 50
num_nodes = 200
tx_range = 5 
max_distance = 5 

all_results = []

# Realiza múltiples simulaciones para recopilar datos
for _ in range(200):
    results = calculate_probabilities(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, False)
    all_results.append(results)

# Organiza los resultados en una estructura de datos adecuada
data = []
for results in all_results:
    data.append({
        'Edges removed domain': results['probability_mc_domain1'],
        'Disjoint paths domain': results['probability_mc_domain3'],
        'Common Neighbor domain': results['probability_mc_domain2']
    })

df = pd.DataFrame(data)
print(df)

# Resumen estadístico
summary = df.describe()
print(summary)

# Boxplot para comparar resultados de los enfoques
plt.figure(figsize=(12, 8))
sns.boxplot(data=df)
plt.title('Comparison of Probabilities for Different Domains')
plt.show()

# CDF plot for each approach
approaches = ['Edges removed domain', 'Disjoint paths domain', 'Common Neighbor domain']

# Graficar el CDF para cada dominio
plt.figure(figsize=(12, 8))
for approach in approaches:
    sns.ecdfplot(data=df, x=approach, label=approach)

plt.title('Cumulative Distribution Function (CDF) of Monte Carlo Probabilities')
plt.xlabel('Probability')
plt.ylabel('Cumulative Probability')
plt.legend(title='Domain')
plt.show()
