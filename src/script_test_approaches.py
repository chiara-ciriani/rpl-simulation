from matplotlib.lines import Line2D
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from test_domains_dio import send_to_all_street_lights
from test_domains_dio_multipath import send_to_all_street_lights_multipath

NUM_STREET_LIGHTS=11

all_results = []

MULTIPATH=True

if MULTIPATH:
    width = 2500
    height = 1800
    # height = 2000
    num_nodes = 200
    tx_range = 200
    # tx_range = 400
    max_distance = 200
else:
    width = 625
    height = 500
    num_nodes = 200
    tx_range = 50
    max_distance = 50

for _ in range(150):
    if MULTIPATH:
        # MULTI PATH
        results, root_position = send_to_all_street_lights_multipath(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, tx_range == max_distance, False)
    else:
        # SINGLE PATH
        results, root_position = send_to_all_street_lights(width, height, num_nodes, NUM_STREET_LIGHTS, tx_range, max_distance, False)
    all_results.append((results, root_position))


data = []
for results, root_position in all_results:
    for sl_id, values in results.items():
        if MULTIPATH:   
            data.append({
                'StreetLight': sl_id,
                'Projected Routes: Edges Removed': values[0],
                'Projected Routes: Nodes Removed': values[1],
                'P2P-MPL: Edges Removed': values[2],
                'P2P-MPL: Nodes Removed': values[3],
                'P2P-MPL: Common Neighbor': values[4],
                'RootX': root_position[0],
                'RootY': root_position[1],
                'num_nodes': num_nodes
            })
        else:
            if not values[0]: continue
            data.append({
                'StreetLight': sl_id,
                'Plain RPL': values[0],
                'RPL with Gateway': values[1],
                'Projected Routes': values[2],
                'P2P-MPL': values[3],
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
if MULTIPATH:
    approaches = ['Projected Routes: Edges Removed', 'Projected Routes: Nodes Removed', 'P2P-MPL: Edges Removed', 'P2P-MPL: Nodes Removed', 'P2P-MPL: Common Neighbor']
    colors = {
    'Projected Routes: Edges Removed': 'red',
    'Projected Routes: Nodes Removed': 'red',
    'P2P-MPL: Edges Removed': 'green',
    'P2P-MPL: Nodes Removed': 'green',
    'P2P-MPL: Common Neighbor': 'green'
    }
    markers = {
    'Projected Routes: Edges Removed': 'o',  # Circulo
    'Projected Routes: Nodes Removed': "X",  # X
    'P2P-MPL: Edges Removed': 'o',  # Circulo
    'P2P-MPL: Nodes Removed': "X",  # X
    'P2P-MPL: Common Neighbor': '^'  # Triángulo
    }
    marker_size = 50
else:
    approaches = ['Plain RPL', 'RPL with Gateway', 'Projected Routes', 'P2P-MPL']
    colors = {
        'Plain RPL': 'blue',
        'RRPL with Gateway': 'orange',
        'Projected Routes': 'red',
        'P2P-MPL': 'green'
    }
    markers = {
    'Plain RPL': "o",  # Circulo
    'RPL with Gateway': "s",  # X
    'Projected Routes': "X",  # Circulo
    'P2P-MPL': ">" # X
    }
    marker_size = 50

plt.figure(figsize=(10, 6))

# Tamaño fijo de la figura en pulgadas
FIGURE_SIZE = (8, 5)  # Ancho x Alto en pulgadas
DPI = 300  # Resolución en puntos por pulgada
X_LIMITS = (0, 350)  # Límite fijo para el eje X
Y_LIMITS = (0, 1)  # Límite fijo para el eje Y
X_TICKS = range(0, 351, 50)  # Divisiones uniformes en X
Y_TICKS = np.linspace(0, 1, 6)  # Divisiones uniformes en Y

# Almacenar elementos de leyenda
legend_elements = []

for sl_id in df['StreetLight'].unique():
    # if sl_id == 0: continue
    subset = df[df['StreetLight'] == sl_id]

    plt.figure(figsize=FIGURE_SIZE)

    for approach in approaches:
        # Generar la línea de ECDF
        ecdf_line = sns.ecdfplot(
            data=subset, 
            x=approach, 
            label=approach, 
            color=colors[approach],  # Asignar color
        )

        # Calcular manualmente el ECDF
        x_values = np.sort(subset[approach].values)
        y_values = np.arange(1, len(x_values)+1) / len(x_values)

        # Dibujar los marcadores solo en puntos espaciados
        marker_indices = np.arange(0, len(x_values), 5)  # Cambia el 5 para ajustar la separación

        plt.scatter(
            x_values[marker_indices], 
            y_values[marker_indices], 
            color=colors[approach], 
            marker=markers[approach], 
            s=marker_size
        )

        # Agregar tanto la línea como el marcador a la leyenda
        legend_elements.append(Line2D([0], [0], color=colors[approach], lw=2, 
                                  label=approach, marker=markers[approach], 
                                  markersize=10, markerfacecolor=colors[approach], 
                                  markeredgewidth=0))  # Esto agrega tanto la línea como el marcador
        
    if not MULTIPATH:   
        # Annotate Projected Routes and Proposed Solution with minimal domain with exact values
        projected_routes_value = subset['Projected Routes'].unique()[0]
        proposed_solution_value = subset['P2P-MPL'].unique()[0]
        
        # Línea y texto para Projected Routes
        plt.axvline(x=projected_routes_value, color='red', linestyle='dotted')  # Línea discontinua para Projected Routes
        plt.text(projected_routes_value + 5, 0.5, f'{projected_routes_value}', color='red', va='center', 
                 ha='left', fontsize=14, fontweight='bold')  # Mover el texto un poco a la derecha (+5 en x)
        
        # Línea y texto para Proposed Solution
        plt.axvline(x=proposed_solution_value, color='green', linestyle='solid')  # Línea continua para Proposed Solution
        plt.text(proposed_solution_value + 5, 0.5, f'{proposed_solution_value}', color='green', va='center', 
         ha='left', fontsize=14, fontweight='bold')  # Mover el texto un poco a la derecha (+5 en x)

    # Configurar los ejes con límites y ticks fijos
    plt.xlim(X_LIMITS)
    plt.ylim(Y_LIMITS)
    plt.xticks(X_TICKS)
    plt.yticks(Y_TICKS)

    # Actualizar el título y las etiquetas
    plt.xlabel('Number of Transmissions', fontsize=14)
    plt.ylabel('Cumulative Probability', fontsize=12)

    # Aumentar el tamaño de fuente para las etiquetas de los ticks
    plt.tick_params(axis='both', which='major', labelsize=14)

    # Añadir líneas de cuadrícula solo en la dirección horizontal
    plt.grid(axis='y', linestyle='--', linewidth=0.7)

    # Crear una lista de elementos de la leyenda
    legend_elements = [Line2D([0], [0], marker=markers[approach], color='w',
                               label=approach, markerfacecolor=colors[approach], markersize=10)
                       for approach in approaches]

    # Mostrar la leyenda
    plt.legend(handles=legend_elements, fontsize=12)
    plt.show()

approaches2 = ['Plain RPL', 'RPL with Gateway']

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

# show_scatter_plot(df)