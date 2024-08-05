import svgwrite

# Create an SVG drawing
dwg = svgwrite.Drawing('calle_horizontal_con_casas_y_persona_v2.svg', profile='tiny')

# Define dimensions
street_height = 50
house_width = 40
house_height = 30
num_houses = 5
street_length = num_houses * house_width * 2
light_radius = 6  # Increased radius for better visibility

# Define colors
street_color = '#888'
house_color = '#555'
roof_color = '#333'
person_color = '#FF0000'
light_color = '#FFD700'

# Draw the street
dwg.add(dwg.rect(insert=(0, house_height), size=(street_length, street_height), fill=street_color))

# Function to draw a house
def draw_house(x, y):
    dwg.add(dwg.rect(insert=(x, y), size=(house_width, house_height), fill=house_color))
    dwg.add(dwg.polygon(points=[(x, y), (x + house_width / 2, y - house_height / 2), (x + house_width, y)], fill=roof_color))

# Draw houses on both sides of the street
for i in range(num_houses):
    x_pos = i * house_width * 2 + house_width / 2
    draw_house(x_pos, 0)  # Top side
    draw_house(x_pos, house_height + street_height)  # Bottom side

# Draw street lights between houses on both sides
light_offset = 10  # Offset from the street edge for the lights
for i in range(num_houses - 1):
    x_pos = (i + 1) * house_width * 2
    dwg.add(dwg.circle(center=(x_pos, house_height - light_offset), r=light_radius, fill=light_color))  # Top side lights
    dwg.add(dwg.circle(center=(x_pos, house_height + street_height + light_offset), r=light_radius, fill=light_color))  # Bottom side lights

# Draw person exiting the middle house (3rd house from the left on the bottom side)
person_x = (2 * house_width * 2) + house_width
person_y = house_height + street_height + house_height / 2
dwg.add(dwg.circle(center=(person_x, person_y), r=5, fill=person_color))

# Save the drawing
dwg.save()

dwg.filename
