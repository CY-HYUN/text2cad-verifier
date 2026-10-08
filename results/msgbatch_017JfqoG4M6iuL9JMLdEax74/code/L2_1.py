import cadquery as cq
import math

L = 50.0
R = 30.0
# place cylinder axis so the arc passes (just inside) the cube's vertical edges
d = L / 2 + math.sqrt(R**2 - (L / 2) ** 2) - 0.05

result = cq.Workplane("XY").box(L, L, L)

for (x, y) in [(d, 0), (-d, 0), (0, d), (0, -d)]:
    cyl = (
        cq.Workplane("XY")
        .workplane(offset=-L)
        .center(x, y)
        .circle(R)
        .extrude(2 * L)
    )
    result = result.cut(cyl)
