import cadquery as cq
import math

cube = cq.Workplane("XY").box(50, 50, 50)
d = 42
r = 30
result = cube
for (x, y) in [(d, 0), (-d, 0), (0, d), (0, -d)]:
    cyl = (cq.Workplane("XY").workplane(offset=-30)
           .center(x, y).circle(r).extrude(60))
    result = result.cut(cyl)
