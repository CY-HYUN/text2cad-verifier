import cadquery as cq
import math

# Create the main octagonal prism body
# Regular octagon with circumscribed circle diameter of 40mm (radius 20mm)
radius = 20
height = 60
sides = 8

# Create the octagonal prism
octagon = cq.Workplane("XY").polygon(sides, radius).extrude(height)

# Create the conical cutting surface for the pointed top using a cone solid
# We'll use the built-in Solid.makeCone method
cone_height = 25  # Height of the cone that creates the point
base_radius = radius * math.sqrt(2)

# Create cone by revolving a triangle
cone_solid = cq.Solid.makeCone(base_radius, 0, cone_height)
cone_wp = cq.Workplane("XY").add(cone_solid)
cone_wp = cone_wp.translate((0, 0, height))

# Cut the cone from the octagonal prism to create the pointed top
result = octagon.cut(cone_wp)

# Add the rectangular groove at the middle (height/2)
groove_y = height / 2
groove_width = 5
groove_depth = 2
groove_length = radius * 5  # Make it long enough to go around

# Create a rectangular box for the groove
groove_box = cq.Workplane("XY").box(groove_length, groove_width, groove_depth)
groove_box = groove_box.translate((0, 0, groove_y))

# Cut the groove from the result
result = result.cut(groove_box)

