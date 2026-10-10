import cadquery as cq
import math

# Create the bottom layer (diameter 60mm, height 10mm)
bottom_layer = cq.Workplane("XY").circle(30).extrude(10)

# Create the middle layer (diameter 40mm, height 10mm)
# Position it at Z=10 (on top of bottom layer)
middle_layer = cq.Workplane("XY").workplane(offset=10).circle(20).extrude(10)

# Create the top layer (diameter 20mm, height 10mm)
# Position it at Z=20 (on top of middle layer)
top_layer = cq.Workplane("XY").workplane(offset=20).circle(10).extrude(10)

# Combine all three layers
result = bottom_layer.union(middle_layer).union(top_layer)
