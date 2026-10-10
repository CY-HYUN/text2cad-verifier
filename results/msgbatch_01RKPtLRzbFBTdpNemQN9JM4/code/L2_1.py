import cadquery as cq
import math

L = 50.0
R = 30.0
d = 25 + math.sqrt(R**2 - 25**2)  # cylinder passes through the vertical edges
d = d - 0.01

box = cq.Workplane("XY").box(L, L, L)
result = box
for ang in (0, 90, 180, 270):
    x = d * math.cos(math.radians(ang))
    y = d * math.sin(math.radians(ang))
    cyl = (cq.Workplane("XY").workplane(offset=-L/2 - 1)
           .center(x, y).circle(R).extrude(L + 2))
    result = result.cut(cyl)
