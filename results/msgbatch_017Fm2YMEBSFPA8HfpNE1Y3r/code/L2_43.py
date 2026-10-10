import cadquery as cq
import math

# Create the base square 60x60 mm and extrude by 20 mm
base = cq.Workplane("XY").box(60, 60, 20, centered=True)

# Cut out the inner square to create a frame
# Create a workplane on XY and cut a 40x40 square through the center
inner_cutout = cq.Workplane("XY").box(40, 40, 20, centered=True)
result = base.cut(inner_cutout)

# Add the cylinder on top
# Create a cylinder with diameter 40 mm (radius 20 mm) and extrude by 20 mm
# Position it at z=10 (top of the base) and extend it 20 mm upward
cylinder = cq.Workplane("XY").circle(20).extrude(20).translate((0, 0, 10))

# Merge the cylinder with the frame structure
result = result.union(cylinder)
