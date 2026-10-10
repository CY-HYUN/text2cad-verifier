import cadquery as cq
import math

# Create a regular hexagon with inscribed circle diameter of 50mm
# For a regular hexagon, if the inscribed circle diameter is d, 
# the circumradius (distance from center to vertex) is R = d / sqrt(3)
inscribed_diameter = 50
circumradius = inscribed_diameter / math.sqrt(3)

# Create the hexagonal prism
hexagon = cq.Workplane("XY").polygon(6, circumradius)
prism = hexagon.extrude(20)

# Create a circular through-hole at the center with diameter 20mm
hole = cq.Workplane("XY").circle(10).extrude(20)
prism = prism.cut(hole)

# Chamfer the six outer edges on the top surface
# The top surface edges are those at z=20
# We need to select and chamfer these edges
prism = prism.faces(">Z").edges().chamfer(2)

result = prism
