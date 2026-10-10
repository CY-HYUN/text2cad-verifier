import cadquery as cq
import math

# Create a hexagon centered at origin with opposite sides horizontal
# For a regular hexagon with inscribed circle diameter (flat-to-flat) of 50mm
# The distance from center to flat edge is 25mm
# For a regular hexagon: side length = inscribed_circle_diameter / sqrt(3)
inscribed_diameter = 50.0
side_length = inscribed_diameter / math.sqrt(3)

# Create the hexagon sketch on XY plane
hex_sketch = (
    cq.Workplane("XY")
    .polygon(6, inscribed_diameter / 2, circumscribed=False)
)

# Extrude the hexagon 20mm in +Z direction
hexagonal_prism = hex_sketch.extrude(20.0)

# Create a sketch on the top face for the through-hole
top_face = hexagonal_prism.faces(">Z").first()
hole_sketch = hexagonal_prism.workplaneFromFace(top_face).circle(25.0)

# Cut through all to create the central through-hole
with_hole = hexagonal_prism.cutThruAll(hole_sketch)

# Apply 45-degree chamfer to the six outer edges of the top face
# Get the top face and its outer edges
top_face_final = with_hole.faces(">Z").first()
outer_edges = top_face_final.edges().filter(lambda e: e.isOuterEdge())

# Apply chamfer to the outer edges
result = with_hole.chamfer(2.0, outer_edges)
