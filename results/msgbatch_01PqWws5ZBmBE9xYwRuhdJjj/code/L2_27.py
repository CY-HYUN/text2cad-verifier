import cadquery as cq
import math

# Create a cylinder with diameter 30 mm and length 50 mm
result = cq.Workplane("XY").cylinder(height=50, radius=15)

# Select the top surface and create a hexagonal pocket
# For a regular hexagon with inscribed circle diameter of 15 mm (radius 7.5 mm)
hex_radius = 7.5  # inscribed circle radius

# Create hexagon vertices
hex_points = []
for i in range(6):
    angle = i * math.pi / 3  # 60 degrees between vertices
    x = hex_radius * math.cos(angle)
    y = hex_radius * math.sin(angle)
    hex_points.append((x, y))

# Create a closed polygon for the hexagon
hex_polygon = [(hex_points[i][0], hex_points[i][1]) for i in range(6)]

# Pocket the hexagon 25 mm deep from the top
result = result.faces(">Z").workplane().polygon(6, hex_radius).cutBlind(-25)

# Select the bottom surface and create a circular hole
# Circle with diameter 15 mm (radius 7.5 mm)
circle_radius = 7.5

# Create a pocket that goes through the remaining part
# The hexagon pocket is 25 mm deep, so we cut from bottom 25 mm to ensure we reach the middle
result = result.faces("<Z").workplane().circle(circle_radius).cutBlind(-25)

