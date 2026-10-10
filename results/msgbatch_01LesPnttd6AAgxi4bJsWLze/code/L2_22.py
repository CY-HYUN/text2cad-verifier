import cadquery as cq
import math

# Start with a cube
cube = cq.Workplane("XY").box(40, 40, 40, centered=True)

# Cut a through-hole with diameter 30mm at the center
hole = cube.faces(">Z").workplane().hole(30)

# Apply chamfers to the four vertical edges
# The four vertical edges are at the corners of the cube
# We need to identify and chamfer them
# For a cube centered at origin with side length 40:
# The vertical edges are at positions like (+20, +20), (+20, -20), (-20, +20), (-20, -20)

# Get all edges and filter for vertical ones
all_edges = hole.edges()

# Filter vertical edges (those parallel to Z axis)
vertical_edges = all_edges.filter(lambda e: abs(e.direction.z) > 0.99)

# Apply 10mm chamfer to all vertical edges
result = vertical_edges.chamfer(10)
