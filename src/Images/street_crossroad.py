import svgwrite

# Create an SVG drawing
dwg = svgwrite.Drawing('crossroad_final_corrected_lights_v3.svg', profile='tiny')

# Define dimensions
street_width = 50
house_width = 40
house_height = 30
num_houses = 5
street_length = num_houses * house_width * 2
light_radius = 6  # Increased radius for better visibility
gap_size = street_width  # Gap size at the intersection

# Define colors
street_color = '#888'
house_color = '#555'
roof_color = '#333'
person_color = '#FF0000'
light_color = '#FFD700'

# Function to draw a house
def draw_house(x, y):
    dwg.add(dwg.rect(insert=(x, y), size=(house_width, house_height), fill=house_color))
    dwg.add(dwg.polygon(points=[(x, y), (x + house_width / 2, y - house_height / 2), (x + house_width, y)], fill=roof_color))

# Draw the horizontal street
dwg.add(dwg.rect(insert=(0, street_length / 2 - street_width / 2), size=(street_length, street_width), fill=street_color))

# Draw the vertical street
dwg.add(dwg.rect(insert=(street_length / 2 - street_width / 2, 0), size=(street_width, street_length), fill=street_color))

# Draw houses on both sides of the horizontal street, avoiding the intersection
for i in range(num_houses):
    x_pos = i * house_width * 2 + house_width / 2
    if x_pos < street_length / 2 - gap_size or x_pos > street_length / 2 + gap_size:
        draw_house(x_pos, street_length / 2 - street_width / 2 - house_height)  # Top side
        draw_house(x_pos, street_length / 2 + street_width / 2)  # Bottom side

# Draw houses on both sides of the vertical street, avoiding the intersection
for i in range(num_houses):
    y_pos = i * house_width * 2 + house_width / 2
    if y_pos < street_length / 2 - gap_size or y_pos > street_length / 2 + gap_size:
        draw_house(street_length / 2 - street_width / 2 - house_width, y_pos)  # Left side
        draw_house(street_length / 2 + street_width / 2, y_pos)  # Right side

# Draw street lights between houses on the horizontal street
light_offset = 10  # Offset from the street edge for the lights
for i in range(num_houses - 1):
    x_pos = (i + 1) * house_width * 2
    if x_pos < street_length / 2 - gap_size or x_pos > street_length / 2 + gap_size:
        dwg.add(dwg.circle(center=(x_pos, street_length / 2 - street_width / 2 - light_offset), r=light_radius, fill=light_color))  # Top side lights
        dwg.add(dwg.circle(center=(x_pos, street_length / 2 + street_width / 2 + light_offset), r=light_radius, fill=light_color))  # Bottom side lights

# Draw street lights between houses on the vertical street, avoiding the intersection
for i in range(num_houses - 1):
    y_pos = (i + 1) * house_width * 2
    if y_pos < street_length / 2 - gap_size or y_pos > street_length / 2 + gap_size:
        dwg.add(dwg.circle(center=(street_length / 2 - street_width / 2 - light_offset, y_pos), r=light_radius, fill=light_color))  # Left side lights
        dwg.add(dwg.circle(center=(street_length / 2 + street_width / 2 + light_offset, y_pos), r=light_radius, fill=light_color))  # Right side lights

# Draw additional street lights at the intersection on the horizontal street, keeping the same x position
dwg.add(dwg.circle(center=(street_length / 2 - street_width / 2 - light_offset, street_length / 2 - gap_size + light_offset), r=light_radius, fill=light_color))  # Above intersection, left side
dwg.add(dwg.circle(center=(street_length / 2 + street_width / 2 + light_offset, street_length / 2 - gap_size + light_offset), r=light_radius, fill=light_color))  # Above intersection, right side
dwg.add(dwg.circle(center=(street_length / 2 - street_width / 2 - light_offset, street_length / 2 + gap_size - light_offset), r=light_radius, fill=light_color))  # Below intersection, left side
dwg.add(dwg.circle(center=(street_length / 2 + street_width / 2 + light_offset, street_length / 2 + gap_size - light_offset), r=light_radius, fill=light_color))  # Below intersection, right side

# Draw person in the middle of the intersection with larger size
person_x = street_length / 2
person_y = street_length / 2
dwg.add(dwg.circle(center=(person_x, person_y), r=10, fill=person_color))  # Increased radius for better visibility

# Save the drawing
dwg.save()

dwg.filename

