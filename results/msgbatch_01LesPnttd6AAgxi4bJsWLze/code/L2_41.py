import cadquery as cq
import math

# Create the main octagonal prism body
# Regular octagon with circumscribed circle diameter of 40mm (radius 20mm)
radius = 20
height = 60
sides = 8

# Calculate the vertices of a regular octagon inscribed in a circle of radius 20
vertices = []
for i in range(sides):
    angle = (2 * math.pi * i) / sides
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    vertices.append((x, y))

# Create the octagonal prism
octagon = cq.Workplane("XY").polygon(sides, radius).extrude(height)

# Create the conical cutting surface for the pointed top
# The cone has its base at the top of the prism and tapers to a point
# We'll create a cone and position it to cut the top
cone_height = 25  # Height of the cone that creates the point
cone = cq.Workplane("XY").cone(radius1=radius*math.sqrt(2), radius2=0, height=cone_height, direct=(0, 0, 1))
cone = cone.translate((0, 0, height))

# Cut the cone from the octagonal prism to create the pointed top
result = octagon.cut(cone)

# Add the rectangular groove at the middle (height/2)
groove_y = height / 2
groove_width = 5
groove_depth = 2
groove_length = radius * 4  # Make it long enough to go around

# Create a rectangular box for the groove
groove_box = cq.Workplane("XY").box(groove_length, groove_width, groove_depth)
groove_box = groove_box.translate((0, 0, groove_y - groove_depth/2))

# Cut the groove from the result
result = result.cut(groove_box)

# Refine the result to ensure it's a proper solid
result = result.val()
