import cadquery as cq
import math

# Start with a cube
cube = cq.Workplane("XY").box(40, 40, 40, centered=True)

# Cut a through-hole with diameter 30mm at the center
hole = cube.faces(">Z").workplane().hole(30)

# Apply chamfers to the four vertical edges
# For a centered cube with side 40, the vertical edges are at the corners
# We'll chamfer all edges that are vertical (at z-direction)
# The cube has 12 edges, 4 are vertical (at the corners)

result = hole

# Chamfer all vertical edges by selecting them geometrically
# Vertical edges connect top and bottom faces
# We can identify them by their position at the corners
edges_to_chamfer = (
    result
    .edges("|Z")  # Select edges parallel to Z axis
)

result = edges_to_chamfer.chamfer(10)

