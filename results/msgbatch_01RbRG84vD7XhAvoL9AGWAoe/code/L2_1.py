import cadquery as cq
import math

L = 50.0
R = 30.0
# Place cylinder axes so the circle passes exactly through the cube's vertical edges
d = L / 2 + math.sqrt(R**2 - (L / 2) ** 2)

result = cq.Workplane("XY").box(L, L, L)

for ang in (0, 90, 180, 270):
    a = math.radians(ang)
    cx, cy = d * math.cos(a), d * math.sin(a)
    cyl = (
        cq.Workplane("XY")
        .workplane(offset=-L)
        .center(cx, cy)
        .circle(R)
        .extrude(2 * L)
    )
    result = result.cut(cyl)
