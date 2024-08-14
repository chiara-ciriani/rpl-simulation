import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from test_domains_probabilities import calculate_probabilities

NUM_STREET_LIGHTS = 11

width = 70
height = 70
num_nodes = 600
tx_range = 5 
max_distance = 5 

data_source_0 = []
data_source_5 = []
data_source_10 = []

# Realiza múltiples simulaciones para recopilar datos
for _ in range(200):
    results = calculate_probabilities(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, False)
    
    data_source_0.append({
        'Edges removed domain': results['probability_mc_domain1_source_0'],
        'Disjoint paths domain': results['probability_mc_domain3_source_0'],
        'Common Neighbor domain': results['probability_mc_domain2_source_0']
    })
    
    data_source_5.append({
        'Edges removed domain': results['probability_mc_domain1_source_5'],
        'Disjoint paths domain': results['probability_mc_domain3_source_5'],
        'Common Neighbor domain': results['probability_mc_domain2_source_5']
    })
    
    data_source_10.append({
        'Edges removed domain': results['probability_mc_domain1_source_10'],
        'Disjoint paths domain': results['probability_mc_domain3_source_10'],
        'Common Neighbor domain': results['probability_mc_domain2_source_10']
    })

df_source_0 = pd.DataFrame(data_source_0)
df_source_5 = pd.DataFrame(data_source_5)
df_source_10 = pd.DataFrame(data_source_10)

# Graficar el CDF para cada origen (SL 0, SL 5, SL 10)
approaches = ['Edges removed domain', 'Disjoint paths domain', 'Common Neighbor domain']

plt.figure(figsize=(12, 8))
for approach in approaches:
    sns.ecdfplot(data=df_source_0, x=approach, label=approach)
plt.title('CDF in a network of 600 nodes and 11 street lights')
plt.xlabel('Probability that all street lights receive message from SL 0')
plt.ylabel('Cumulative Probability')
plt.legend(title='Domain')
plt.show()

plt.figure(figsize=(12, 8))
for approach in approaches:
    sns.ecdfplot(data=df_source_5, x=approach, label=approach)
plt.title('CDF in a network of 600 nodes and 11 street lights')
plt.xlabel('Probability that all street lights receive message from SL 5')
plt.ylabel('Cumulative Probability')
plt.legend(title='Domain')
plt.show()

plt.figure(figsize=(12, 8))
for approach in approaches:
    sns.ecdfplot(data=df_source_10, x=approach, label=approach)
plt.title('CDF in a network of 600 nodes and 11 street lights')
plt.xlabel('Probability that all street lights receive message from SL 10')
plt.ylabel('Cumulative Probability')
plt.legend(title='Domain')
plt.show()
