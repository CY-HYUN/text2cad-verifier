import cadquery as cq
import math

# Rectangular block: X from 0 to 60, Y from -20 to 20, thickness 10 in Z
rect = cq.Workplane("XY").box(60, 40, 10, centered=(False, True, False))

# Half-cylinder on the right: radius 20, centered at x=60, extending to x=80
cyl = cq.Workplane("XY").center(60, 0).circle(20).extrude(10)
half_mask = cq.Workplane("XY").box(20, 40, 10, centered=(False, True, False)).translate((60, 0, 0))
half_cyl = cyl.intersect(half_mask)

result = rect.union(half_cyl)
