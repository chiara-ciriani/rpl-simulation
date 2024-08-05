import svgwrite
import math

# Crear un nuevo dibujo SVG
dwg = svgwrite.Drawing('network_graph_adjusted.svg', profile='tiny')

# Definir colores para los caminos
path_colors = ['#FF00FF', '#8FBC8F', '#800080', '#FF0000']  # Path 1, Path 2, Path 3, Path 4

# Definir las posiciones de los nodos (x, y)
node_positions = {
    0: (50, 150),
    1: (250, 150),
    2: (450, 150),
    7: (150, 50),
    14: (150, 250),
    21: (50, 250),
    8: (350, 250),
    9: (450, 250)
}

# Definir las conexiones y sus calidades
connections = [
    (0, 7, 0.91), (0, 14, 0.66), (0, 21, 0.94),
    (1, 0, 0.74), (1, 2, 0.72), (1, 14, 0.91),
    (1, 8, 0.73), (2, 9, 0.67), (7, 1, 0.73),
    (8, 9, 0.79), (9, 8, 0.75), (14, 21, 0.82),
    (14, 8, 0.61), (14, 1, 0.74)
]

# Definir los caminos y sus colores
paths = {
    'Path 1': [(0, 7), (7, 1), (1, 2)],
    'Path 2': [(0, 1), (1, 2)],
    'Path 3': [(0, 14), (14, 1), (1, 2)],
    'Path 4': [(0, 21), (21, 14), (14, 1), (1, 2)]
}

# Función para ajustar la posición de la flecha para que no salga del centro del nodo
def adjust_position(start, end, offset=20):
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    start_x = start[0] + offset * math.cos(angle)
    start_y = start[1] + offset * math.sin(angle)
    end_x = end[0] - offset * math.cos(angle)
    end_y = end[1] - offset * math.sin(angle)
    return (start_x, start_y), (end_x, end_y)

# Dibujar los nodos
for node, (x, y) in node_positions.items():
    if node in [0, 1, 2]:  # Nodos de street lights
        dwg.add(dwg.circle(center=(x, y), r=20, fill='blue'))
    else:
        dwg.add(dwg.circle(center=(x, y), r=15, fill='darkgray'))
    dwg.add(dwg.text(str(node), insert=(x - 5, y + 5), fill='white'))

# Dibujar las conexiones
for (start, end, quality) in connections:
    start_pos = node_positions[start]
    end_pos = node_positions[end]
    adjusted_start, adjusted_end = adjust_position(start_pos, end_pos)
    dwg.add(dwg.line(start=adjusted_start, end=adjusted_end, stroke='black', stroke_width=2))
    text_x = (adjusted_start[0] + adjusted_end[0]) / 2
    text_y = (adjusted_start[1] + adjusted_end[1]) / 2
    dwg.add(dwg.text(f'{quality:.2f}', insert=(text_x, text_y), fill='black'))

# Dibujar los caminos
for i, (path_name, path) in enumerate(paths.items()):
    color = path_colors[i]
    for (start, end) in path:
        start_pos = node_positions[start]
        end_pos = node_positions[end]
        adjusted_start, adjusted_end = adjust_position(start_pos, end_pos)
        dwg.add(dwg.line(start=adjusted_start, end=adjusted_end, stroke=color, stroke_width=4, opacity=0.7))
    # Agregar la leyenda del camino
    dwg.add(dwg.text(path_name, insert=(10, 30 + i * 20), fill=color, font_size='15px', font_weight='bold'))

# Guardar el dibujo
dwg.save()

print("SVG saved as 'network_graph_adjusted.svg'")
