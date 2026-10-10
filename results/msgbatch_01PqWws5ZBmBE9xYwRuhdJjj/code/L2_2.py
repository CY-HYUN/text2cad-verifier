import cadquery as cq
import math

# Create a sphere with radius 40 mm centered at the origin
sphere = cq.Workplane("XY").sphere(40)

# Create a workplane on XY plane and draw a circle with diameter 30 mm (radius 15 mm)
# centered at X = 25 mm, Y = 0
cut_workplane = cq.Workplane("XY").moveTo(25, 0)

# Draw a circle with diameter 30 mm and extrude it as a cut through the entire part
# The circle will be extruded along Z-axis through the entire sphere
cylinder_cut = cut_workplane.circle(15).cutThruAll()

# Perform the cut operation on the sphere
result = sphere.cut(cylinder_cut)
