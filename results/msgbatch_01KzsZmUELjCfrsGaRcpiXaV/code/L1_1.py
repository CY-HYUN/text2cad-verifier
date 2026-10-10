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
prism = prism.faces(">Z").workplane().hole(20)

# Chamfer the six outer edges on the top surface
# Select edges that are on the top face and are part of the hexagon perimeter
prism = prism.edges(">Z and not <Z").chamfer(2)

result = prism
